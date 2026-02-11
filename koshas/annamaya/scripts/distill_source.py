#!/usr/bin/env python3
"""
distill_source.py - PDF Source Distillation Pipeline for Tryambakam Noesis

Processes extracted PDF content (raw_text.txt) into structured SOURCE.md and 
DISTILLED.md files for integration into the Vedic Runtime Source Memory.

Usage:
    python3 distill_source.py --staging-dir <path> --output-dir <path> [--source-name <name>]
    python3 distill_source.py --list-staging <path>

Examples:
    # List available sources in staging
    python3 distill_source.py --list-staging staging/vedic-runtime-source-memory

    # Process a single source
    python3 distill_source.py \
        --staging-dir staging/vedic-runtime-source-memory/vedic-studies \
        --output-dir koshas/manomaya/source-memory/vedic-studies \
        --source-name "Vedic Studies"

    # Process with auto-detected name
    python3 distill_source.py \
        --staging-dir staging/vedic-runtime-source-memory/clifford-algebras \
        --output-dir koshas/manomaya/source-memory/clifford-algebras

Author: Tryambakam Noesis / Chitta Weaver
Created: 2026-02-11
"""

import argparse
import os
from pathlib import Path
from datetime import datetime
import shutil


def list_staging_sources(staging_root: Path) -> list[dict]:
    """List all source directories in staging with their status."""
    sources = []
    
    if not staging_root.exists():
        print(f"❌ Staging directory not found: {staging_root}")
        return sources
    
    for item in sorted(staging_root.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            source_info = {
                'name': item.name,
                'path': item,
                'has_pdf': False,
                'has_extraction': False,
                'has_raw_text': False,
                'has_images': False,
                'pdf_name': None,
                'text_lines': 0
            }
            
            # Check for PDF
            pdfs = list(item.glob('*.pdf'))
            if pdfs:
                source_info['has_pdf'] = True
                source_info['pdf_name'] = pdfs[0].name
            
            # Check for extraction directory
            extraction_dir = item / 'extraction'
            if extraction_dir.exists():
                source_info['has_extraction'] = True
                
                raw_text = extraction_dir / 'raw_text.txt'
                if raw_text.exists():
                    source_info['has_raw_text'] = True
                    source_info['text_lines'] = sum(1 for _ in open(raw_text))
                
                images_dir = extraction_dir / 'images'
                if images_dir.exists() and any(images_dir.iterdir()):
                    source_info['has_images'] = True
            
            sources.append(source_info)
    
    return sources


def print_staging_status(sources: list[dict]) -> None:
    """Print formatted status of staging sources."""
    print("\n📦 Staging Sources Status\n")
    print(f"{'Source':<45} {'PDF':^5} {'Text':^5} {'Imgs':^5} {'Lines':>8}")
    print("-" * 75)
    
    for src in sources:
        pdf_status = "✅" if src['has_pdf'] else "❌"
        text_status = "✅" if src['has_raw_text'] else "❌"
        img_status = "✅" if src['has_images'] else "—"
        lines = str(src['text_lines']) if src['has_raw_text'] else "—"
        
        name = src['name'][:44] if len(src['name']) > 44 else src['name']
        print(f"{name:<45} {pdf_status:^5} {text_status:^5} {img_status:^5} {lines:>8}")
    
    print("\n" + "-" * 75)
    print(f"Total: {len(sources)} sources")


def generate_source_md(
    source_name: str,
    staging_dir: Path,
    pdf_name: str | None,
    extraction_date: str
) -> str:
    """Generate SOURCE.md content."""
    
    # Derive author/type from directory name or leave as placeholder
    template = f"""# SOURCE: {source_name}

**Type:** PDF Document
**Author:** [Author - to be filled]
**Original Location:** `{staging_dir.relative_to(staging_dir.parent.parent) if staging_dir.parent.parent.exists() else staging_dir}`{f'/{pdf_name}' if pdf_name else ''}

**Extraction Date:** {extraction_date}
**Extracted To:** `{staging_dir.relative_to(staging_dir.parent.parent) if staging_dir.parent.parent.exists() else staging_dir}/extraction/raw_text.txt`

---

## 📋 Document Summary

[TODO: Add document summary - describe the main topics and purpose]

---

## 🎯 Key Contributions to Tryambakam Noesis

| Concept | Integration Target | Status |
|---------|-------------------|--------|
| [Concept 1] | [[TARGET-FILE]] | ⏳ Pending |
| [Concept 2] | [[TARGET-FILE]] | ⏳ Pending |

---

## 📚 Citation

```
[TODO: Add proper citation]
```

---

## 🔗 Related Sources

- [[MOC-VEDIC-RUNTIME]] → Parent index

---

**Provenance verified.** ✅
"""
    return template


def generate_distilled_md(
    source_name: str,
    raw_text_preview: str,
    extraction_date: str
) -> str:
    """Generate DISTILLED.md template with preview of raw text."""
    
    template = f"""# DISTILLED: {source_name}

**Source:** [[{source_name.lower().replace(' ', '-')}-SOURCE]]
**Distillation Date:** {extraction_date}

---

## 🎯 Core Thesis

[TODO: Summarize the central argument or purpose of this document in 2-3 sentences]

---

## 📊 Key Extractions

### Section 1: [Topic]

[Extract key information here]

### Section 2: [Topic]

[Extract key information here]

---

## 💡 Key Insights

1. **[Insight 1]** — [Explanation]
2. **[Insight 2]** — [Explanation]
3. **[Insight 3]** — [Explanation]

---

## 🔮 Tryambakam Mapping

| Source Concept | Tryambakam Integration | Notes |
|----------------|----------------------|-------|
| [Concept] | [[TARGET]] | [How it integrates] |

---

## 📝 Raw Text Preview (First 100 Lines)

```
{raw_text_preview}
```

---

## 🔗 Integration Points

- [[VEDIC-LEXICON]] — Tatva framework
- [[CLIFFORD-MOOLAKAPRITHI-ALGEBRA]] — Mathematical foundations
- [[MOC-VEDIC-RUNTIME]] → Parent index

---

**Distillation complete.** ✅
"""
    return template


def copy_images(staging_dir: Path, output_dir: Path) -> int:
    """Copy extracted images to output directory."""
    images_src = staging_dir / 'extraction' / 'images'
    images_dst = output_dir / 'images'
    
    if not images_src.exists():
        return 0
    
    image_files = list(images_src.glob('*'))
    if not image_files:
        return 0
    
    images_dst.mkdir(parents=True, exist_ok=True)
    
    copied = 0
    for img in image_files:
        if img.is_file():
            shutil.copy2(img, images_dst / img.name)
            copied += 1
    
    return copied


def process_source(
    staging_dir: Path,
    output_dir: Path,
    source_name: str | None = None
) -> bool:
    """Process a single source from staging to output."""
    
    # Validate staging directory
    if not staging_dir.exists():
        print(f"❌ Staging directory not found: {staging_dir}")
        return False
    
    extraction_dir = staging_dir / 'extraction'
    raw_text_file = extraction_dir / 'raw_text.txt'
    
    if not raw_text_file.exists():
        print(f"❌ No raw_text.txt found in {extraction_dir}")
        return False
    
    # Auto-detect source name if not provided
    if source_name is None:
        source_name = staging_dir.name.replace('-', ' ').title()
    
    # Find PDF name
    pdfs = list(staging_dir.glob('*.pdf'))
    pdf_name = pdfs[0].name if pdfs else None
    
    # Read raw text preview
    with open(raw_text_file, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()[:100]
        raw_text_preview = ''.join(lines)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    extraction_date = datetime.now().strftime('%Y-%m-%d')
    
    # Generate SOURCE.md
    source_md = generate_source_md(source_name, staging_dir, pdf_name, extraction_date)
    source_path = output_dir / 'SOURCE.md'
    
    if source_path.exists():
        print(f"⚠️  SOURCE.md already exists, skipping: {source_path}")
    else:
        with open(source_path, 'w') as f:
            f.write(source_md)
        print(f"✅ Created: {source_path}")
    
    # Generate DISTILLED.md
    distilled_md = generate_distilled_md(source_name, raw_text_preview, extraction_date)
    distilled_path = output_dir / 'DISTILLED.md'
    
    if distilled_path.exists():
        print(f"⚠️  DISTILLED.md already exists, skipping: {distilled_path}")
    else:
        with open(distilled_path, 'w') as f:
            f.write(distilled_md)
        print(f"✅ Created: {distilled_path}")
    
    # Copy images
    images_copied = copy_images(staging_dir, output_dir)
    if images_copied > 0:
        print(f"✅ Copied {images_copied} images to {output_dir / 'images'}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='PDF Source Distillation Pipeline for Tryambakam Noesis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List available sources in staging
    python3 distill_source.py --list-staging staging/vedic-runtime-source-memory

    # Process a single source
    python3 distill_source.py \\
        --staging-dir staging/vedic-runtime-source-memory/vedic-studies \\
        --output-dir koshas/manomaya/source-memory/vedic-studies \\
        --source-name "Vedic Studies"
        """
    )
    
    parser.add_argument(
        '--list-staging',
        type=Path,
        metavar='PATH',
        help='List all sources in staging directory'
    )
    
    parser.add_argument(
        '--staging-dir',
        type=Path,
        metavar='PATH',
        help='Path to staging source directory (with extraction/raw_text.txt)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        metavar='PATH',
        help='Path to output directory for SOURCE.md and DISTILLED.md'
    )
    
    parser.add_argument(
        '--source-name',
        type=str,
        metavar='NAME',
        help='Human-readable source name (auto-detected from directory if not provided)'
    )
    
    args = parser.parse_args()
    
    # Handle --list-staging
    if args.list_staging:
        sources = list_staging_sources(args.list_staging)
        print_staging_status(sources)
        return
    
    # Handle processing
    if args.staging_dir and args.output_dir:
        success = process_source(
            args.staging_dir,
            args.output_dir,
            args.source_name
        )
        if success:
            print(f"\n✅ Processing complete for: {args.source_name or args.staging_dir.name}")
        else:
            print(f"\n❌ Processing failed")
            exit(1)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
