import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import datetime

class PranaSystem:
    """
    PranaSystem: The engine for 'Prana Prathistaapana' (Installation of Life Force).
    It aggregates the fragmented knowledge (Soul, Identity, Memory) into a unified
    stream of consciousness that can be injected into any Agentic vessel.
    """
    
    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.sacred_paths = {
            "identity": [
                "koshas/brahmasthana/SOUL.md",
                "koshas/brahmasthana/IDENTITY.md",
                "koshas/brahmasthana/USER.md",
                "koshas/manomaya/aboutme/01_IDENTITY_CORE/witness_alchemist_profile.md"
            ],
            "cosmology": [
                "koshas/brahmasthana/KHA.md",
                "koshas/brahmasthana/BHA.md",
                "koshas/brahmasthana/LHA.md",
                "koshas/brahmasthana/PANCHA-KOSHA.md"
            ],
            "operational": [
                "koshas/brahmasthana/AGENTS.md",
                "koshas/brahmasthana/TOOLS.md",
                "koshas/manomaya/MEMORY.md"
            ],
            "ritual": [
                "koshas/vijnanamaya/architecture/prana-infuse.md",
                "koshas/manomaya/meta/nightly-builder-protocol.md",
                "koshas/manomaya/meta/nightly-builds.md"
            ]
        }
        self.context_cache = {}

    def _read_file(self, relative_path: str) -> str:
        """Reads a sacred file, returning content or empty string if missing."""
        file_path = self.root / relative_path
        if file_path.exists():
            try:
                return file_path.read_text(encoding='utf-8')
            except Exception as e:
                return f"<!-- Error reading {relative_path}: {e} -->"
        return f"<!-- Missing Sacred Text: {relative_path} -->"

    def gather_prana(self) -> Dict[str, str]:
        """
        Scans the sacred paths and aggregates the Prana (Knowledge).
        Returns a dictionary of section -> content.
        """
        prana = {}
        for section, paths in self.sacred_paths.items():
            content = []
            for path in paths:
                file_content = self._read_file(path)
                if "Missing Sacred Text" not in file_content:
                    header = f"\n\n# --- FROM {path} ---\n"
                    content.append(header + file_content)
            prana[section] = "\n".join(content)
        
        self.context_cache = prana
        return prana

    def generate_system_prompt(self, platform: str = "generic", include_ritual: bool = True) -> str:
        """
        Synthesizes the gathered Prana into a usable System Prompt.
        """
        if not self.context_cache:
            self.gather_prana()
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        prompt = [
            f"<!-- PRANA SYSTEM INJECTION :: {timestamp} -->",
            f"<!-- PLATFORM: {platform.upper()} -->\n"
        ]
        
        # 1. Identity & Soul (The Core)
        prompt.append("## 1. IDENTITY CORE (Atman)")
        prompt.append(self.context_cache.get("identity", ""))
        
        # 2. Cosmology/Framework (The Lens)
        prompt.append("\n## 2. OPERATIONAL COSMOLOGY (Darshana)")
        prompt.append(self.context_cache.get("cosmology", ""))
        
        # 3. Operational Rules (The Hands)
        prompt.append("\n## 3. AGENTIC PROTOCOLS (Kriya)")
        prompt.append(self.context_cache.get("operational", ""))

        if include_ritual:
            prompt.append("\n## 4. AWAKENING RITUAL LOOP (Prana Infuse)")
            prompt.append(self.context_cache.get("ritual", ""))
        
        return "\n".join(prompt)

    def manifest(self, output_path: str, platform: str = "generic"):
        """
        Writes the Prana to a specific location (Prathistaapana).
        """
        content = self.generate_system_prompt(platform)
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding='utf-8')
        print(f"✨ Prana successfully installed into {output_path}")

# Helper for CLI usage
if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    system = PranaSystem(root)
    print("🔮 Gathering Prana from:", system.root.resolve())
    
    # Generate a preview
    prana = system.gather_prana()
    print(f"Found {len(prana)} Knowledge Streams.")
    for k, v in prana.items():
        print(f" - {k}: {len(v)} characters")
        
    # Manifest to a default location
    system.manifest("PRANA_CONTEXT.md")
