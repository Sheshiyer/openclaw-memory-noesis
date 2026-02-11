#!/usr/bin/env python3
"""
daily_practice_selemene.py — Morning alignment via Selemene Engine

Pulls live data from Selemene API and generates daily practice recommendations.
Designed to run as a cron job at 06:00 IST.

Usage:
    python3 daily_practice_selemene.py              # Full report
    python3 daily_practice_selemene.py --brief      # Short summary
    python3 daily_practice_selemene.py --json       # JSON output
    python3 daily_practice_selemene.py --log        # Append to daily log

Cron entry (06:00 IST = 00:30 UTC):
    30 0 * * * cd /path/to/10865xseed && python3 koshas/annamaya/scripts/daily_practice_selemene.py --log
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from selemene_client import SelemeneClient, SHESH_BIRTH_DATA, SelemeneError

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

REPO_ROOT = SCRIPT_DIR.parent.parent.parent
LOG_DIR = REPO_ROOT / "koshas" / "pranamaya" / "khaloree"

# ═══════════════════════════════════════════════════════════════════════════════
# Formatters
# ═══════════════════════════════════════════════════════════════════════════════

def format_biorhythm(data: dict) -> str:
    """Format biorhythm data for display."""
    lines = ["## 🌊 Biorhythm Cycles"]
    
    for cycle in ["physical", "emotional", "intellectual", "intuitive"]:
        if cycle in data:
            c = data[cycle]
            phase = c.get("phase", "Unknown")
            pct = c.get("percentage", 0)
            critical = "⚠️ CRITICAL" if c.get("is_critical") else ""
            lines.append(f"- **{cycle.title()}:** {pct:.0f}% ({phase}) {critical}")
    
    lines.append(f"- **Overall Energy:** {data.get('overall_energy', 0):.0f}%")
    
    if data.get("critical_days"):
        lines.append(f"\n**Critical Days:** {', '.join(data['critical_days'][:3])}")
    
    return "\n".join(lines)


def format_vedic_clock(data: dict) -> str:
    """Format vedic clock data for display."""
    lines = ["## 🕐 Vedic Clock"]
    
    organ = data.get("current_organ", {})
    dosha = data.get("current_dosha", {})
    
    lines.append(f"- **Organ:** {organ.get('organ', 'Unknown')} ({organ.get('element', '')})")
    lines.append(f"- **Time Window:** {organ.get('time_window', '')}")
    lines.append(f"- **Dosha:** {dosha.get('dosha', 'Unknown')}")
    
    if organ.get("recommended_activities"):
        lines.append("\n**Recommended Activities:**")
        for act in organ["recommended_activities"][:3]:
            lines.append(f"  - {act}")
    
    return "\n".join(lines)


def format_panchanga(data: dict) -> str:
    """Format panchanga data for display."""
    lines = ["## 🌙 Panchanga"]
    
    if "tithi" in data:
        t = data["tithi"]
        lines.append(f"- **Tithi:** {t.get('name', '')} ({t.get('paksha', '')})")
    
    if "nakshatra" in data:
        n = data["nakshatra"]
        lines.append(f"- **Nakshatra:** {n.get('name', '')} (ruled by {n.get('lord', '')})")
    
    if "yoga" in data:
        lines.append(f"- **Yoga:** {data['yoga'].get('name', '')}")
    
    if "karana" in data:
        lines.append(f"- **Karana:** {data['karana'].get('name', '')}")
    
    if "vara" in data:
        lines.append(f"- **Vara:** {data['vara'].get('name', '')} ({data['vara'].get('lord', '')})")
    
    return "\n".join(lines)


def format_dasha(data: dict) -> str:
    """Format vimshottari dasha for display."""
    lines = ["## 🪐 Current Dasha"]
    
    current = data.get("current_period", {})
    
    if "mahadasha" in current:
        m = current["mahadasha"]
        lines.append(f"- **Mahadasha:** {m.get('planet', '')} ({m.get('years', '')} years)")
    
    if "antardasha" in current:
        a = current["antardasha"]
        lines.append(f"- **Antardasha:** {a.get('planet', '')} (until {a.get('end', '')[:10]})")
    
    if "pratyantardasha" in current:
        p = current["pratyantardasha"]
        lines.append(f"- **Pratyantardasha:** {p.get('planet', '')} (until {p.get('end', '')[:10]})")
    
    enrichment = data.get("period_enrichment", {})
    if enrichment.get("pratyantardasha_themes"):
        lines.append(f"\n**Current Themes:** {', '.join(enrichment['pratyantardasha_themes'])}")
    
    return "\n".join(lines)


def format_brief(biorhythm: dict, vedic_clock: dict, dasha: dict) -> str:
    """Generate brief one-line summary."""
    energy = biorhythm.get("overall_energy", 0)
    dosha = vedic_clock.get("current_dosha", {}).get("dosha", "?")
    organ = vedic_clock.get("current_organ", {}).get("organ", "?")
    pratyantar = dasha.get("current_period", {}).get("pratyantardasha", {}).get("planet", "?")
    
    critical = "⚠️ " if biorhythm.get("physical", {}).get("is_critical") else ""
    
    return f"{critical}Energy: {energy:.0f}% | Dosha: {dosha} | Organ: {organ} | Pratyantar: {pratyantar}"


# ═══════════════════════════════════════════════════════════════════════════════
# Main Logic
# ═══════════════════════════════════════════════════════════════════════════════

def fetch_daily_data(client: SelemeneClient) -> dict:
    """Fetch all daily practice data from Selemene."""
    data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "birth_data": SHESH_BIRTH_DATA.to_dict()
    }
    
    # Biorhythm
    try:
        result = client.biorhythm(SHESH_BIRTH_DATA)
        data["biorhythm"] = result.result
        data["biorhythm_prompt"] = result.witness_prompt
    except SelemeneError as e:
        data["biorhythm_error"] = str(e)
    
    # Vedic Clock
    try:
        result = client.vedic_clock()
        data["vedic_clock"] = result.result
    except SelemeneError as e:
        data["vedic_clock_error"] = str(e)
    
    # Panchanga
    try:
        result = client.panchanga(SHESH_BIRTH_DATA)
        data["panchanga"] = result.result
    except SelemeneError as e:
        data["panchanga_error"] = str(e)
    
    # Vimshottari
    try:
        result = client.vimshottari(SHESH_BIRTH_DATA)
        data["vimshottari"] = result.result
    except SelemeneError as e:
        data["vimshottari_error"] = str(e)
    
    return data


def generate_report(data: dict) -> str:
    """Generate full markdown report."""
    now = datetime.now(timezone.utc)
    lines = [
        f"# Daily Practice Report — {now.strftime('%Y-%m-%d')}",
        f"*Generated: {now.strftime('%H:%M UTC')} via Selemene Engine*",
        "",
        "---",
        ""
    ]
    
    if "biorhythm" in data:
        lines.append(format_biorhythm(data["biorhythm"]))
        lines.append("")
    
    if "vedic_clock" in data:
        lines.append(format_vedic_clock(data["vedic_clock"]))
        lines.append("")
    
    if "panchanga" in data:
        lines.append(format_panchanga(data["panchanga"]))
        lines.append("")
    
    if "vimshottari" in data:
        lines.append(format_dasha(data["vimshottari"]))
        lines.append("")
    
    # Witness prompts
    if data.get("biorhythm_prompt"):
        lines.extend([
            "---",
            "",
            "## 🔮 Witness Prompt",
            f"*{data['biorhythm_prompt']}*",
            ""
        ])
    
    # Synthesis
    lines.extend([
        "---",
        "",
        "## 📋 Today's Focus",
        ""
    ])
    
    # Generate focus based on data
    if "vedic_clock" in data:
        activities = data["vedic_clock"].get("current_organ", {}).get("recommended_activities", [])
        if activities:
            lines.append(f"**Morning:** {activities[0] if activities else 'Rest and observe'}")
    
    if "biorhythm" in data:
        energy = data["biorhythm"].get("overall_energy", 50)
        if energy < 30:
            lines.append("**Energy:** Low — prioritize rest, grounding, Apana breathwork")
        elif energy < 60:
            lines.append("**Energy:** Moderate — steady work, avoid overextension")
        else:
            lines.append("**Energy:** High — tackle complex synthesis, Udana breathwork")
    
    if "vimshottari" in data:
        themes = data["vimshottari"].get("period_enrichment", {}).get("pratyantardasha_themes", [])
        if themes:
            lines.append(f"**Dasha Theme:** {', '.join(themes)}")
    
    return "\n".join(lines)


def save_log(data: dict, report: str):
    """Save daily log to pranamaya/khaloree/."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Save JSON data
    json_path = LOG_DIR / f"{today}-selemene.json"
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    
    # Save markdown report
    md_path = LOG_DIR / f"{today}-daily-practice.md"
    with open(md_path, "w") as f:
        f.write(report)
    
    print(f"Logged to: {LOG_DIR}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Daily Practice via Selemene Engine")
    parser.add_argument("--brief", action="store_true", help="One-line summary")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--log", action="store_true", help="Save to daily log")
    
    args = parser.parse_args()
    
    try:
        client = SelemeneClient()
    except SelemeneError as e:
        print(f"Error: {e}")
        print("Set NOESIS_API_KEY environment variable")
        sys.exit(1)
    
    # Fetch data
    data = fetch_daily_data(client)
    
    if args.json:
        print(json.dumps(data, indent=2, default=str))
        return
    
    if args.brief:
        brief = format_brief(
            data.get("biorhythm", {}),
            data.get("vedic_clock", {}),
            data.get("vimshottari", {})
        )
        print(brief)
        return
    
    # Full report
    report = generate_report(data)
    print(report)
    
    if args.log:
        save_log(data, report)


if __name__ == "__main__":
    main()
