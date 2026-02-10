# Vault Agent Context (Root)
`Runtime: 2026-01-26 | Skills-Based Architecture v3.0`

This vault is not a generic cleanup. It is a living knowledgebase engineered around PARA with an **Enneagram + Greek Muses framework** and endocrine overlays. The goal is high-fidelity indexing, tagging, and cross-linking so content can evolve across Projects, Areas, Resources, and Archives without losing context.

> 🎯 **System Update (v3.0)**: Now uses Skills-based architecture with reality-tested Enneagram+PARA taxonomy proven on 3,565 files. Old 68-tag system and Python orchestrator have been replaced.

## Core Intent
- Treat content as a system that evolves across time, not a static archive.
- Preserve provenance and filenames; avoid destructive edits to source files.
- Use Enneagram+PARA classification + indices to drive meaning, not just file placement.
- Process new content through `.claude/skills/` 6-stage pipeline.

## PARA Definitions (Operating Rules)
- **01-Projects** (1.6%): Active, time-bound initiatives and builds (e.g., Phassion/Research).
- **02-Areas** (9.4%): Ongoing responsibilities or domains of mastery (Skills-Development).
- **03-Resources** (89.0%): Reference material and source inputs (books, PDFs, media) - DOMINANT.
- **04-Archives** (0.0%): Completed or inactive projects, historical material (not currently used).
- **processing-folder**: Intake and staging. Nothing is "done" until classified + indexed + placed.

## High-Level Structure (Key Domains)
- **01-Projects**
  - Core-Framework, Runtime-Systems, Products, TheWhyChromosome-Brand, Three-Body-Kingdom, Tryambakam-Noesis.
- **02-Areas**
  - Muse-Enneagram-Framework, Consciousness-Models, Technical-Mystical-Integration, Brand Architecture/Identity, Content-System.
- **03-Resources**
  - Technical, Sacred-Science, Spirituality-Esoteric, Research, Video-Analysis, Authors, Business, Design, Media, Psychology.
- **04-Archives**
  - Historical/completed material.
- **_System**
  - Indices, Tags, Templates, structure docs, scripts, reports.

## Enneagram + Muse Framework (Core Classification System)
This is the primary dimension for content classification and cross-linking.

**Reality-Tested Distribution** (from 3,565 files):
- **Type 5** (75.5%) - Melpomene (Investigator) → Cortisol - Research/knowledge
- **Type 3** (5.5%) - Euterpe (Achiever/Healer) → Endorphins - Health/wellness
- **Type 8** (4.9%) - Terpsichore (Challenger) → Adrenaline - Power/systems
- **Type 1** (4.2%) - Polymnia (Reformer) → Melatonin - Sacred geometry
- **Type 4** (3.9%) - Thalia (Individualist) → Dopamine - Occult/mysticism
- **Type 7** (2.2%) - Calliope (Enthusiast) → Testosterone - Hidden history
- **Type 6** (1.5%) - Erato (Loyalist) → Estrogen - Law/security
- **Type 9** (1.3%) - Urania (Peacemaker) → Serotonin - Consciousness
- **Type 2** (1.0%) - Clio (Helper) → Oxytocin - Personal development

### Required Classification Fields (for new content)
- `enneagram_type` (Type 1-9 with name)
- `greek_muse` (Associated muse archetype)
- `hormone` (Primary hormone mapping)
- `para_bucket` (Resources/Areas/Projects/Archives)
- `domain` (One of 35 proven subdomain paths)
- `moc_links` (Links to relevant library indices)
- `classification_confidence` (min 0.600, avg 0.623)

**Automation**: Use `.claude/skills/orchestrator-skill` for automatic classification through 6-stage pipeline.

### Framework Documentation
- **Core Mapping Source**: `02-Areas/Muse-Enneagram-Framework/muse-enneagram-matrix.md`
- **Endocrine Overlay**: `02-Areas/Muse-Enneagram-Framework/Endocrine-Muse-Matrix/Endocrine-Muse-Integration.md`
- **Framework Index**: `02-Areas/Muse-Enneagram-Framework/_index.md`
- **Taxonomy Reference**: `_System/TAXONOMY-REFERENCE.md` (quick lookup)
- **Single Source of Truth**: `.claude/skills/shared/controlled-vocabulary.yaml`

## Skills-Based Processing System (NEW v3.0)
Located in `.claude/skills/` - 7 modular skills for content processing:

**6-Stage Pipeline**:
1. **discovery-skill** - File inventory + SHA-256 hashing
2. **extraction-skill** - Text extraction (PDF/EPUB)
3. **analysis-skill** - Enneagram+PARA classification ⭐ CORE
4. **routing-skill** - Destination path mapping (35 domains)
5. **processing-skill** - Markdown wrapper generation
6. **integration-skill** - MOC updates

**Meta-Coordinator**:
7. **orchestrator-skill** - Runs all 6 stages with quality gates

**Documentation**: See `_System/SKILLS-REFERENCE.md` for complete guide.

## Tagging System (Modernized)
- **Primary**: Enneagram+PARA taxonomy (9 types + 35 domains)
- **Legacy tags**: Can still use for backward compatibility
- **Taxonomy reference**: `_System/TAXONOMY-REFERENCE.md`
- **Migration guide**: `_System/MIGRATION-GUIDE.md` (old 68-tag system → new)

## Indices and Knowledge Maps
- Master index: `_System/Indices/00-master-index.md`
- Vault structure: `_System/structure/vault-structure.md`
- Maps of content: `_System/structure/maps-of-content.md`

## Processing Flow (Engineering View)
1) Inventory intake (processing-folder)
2) Identify content type + domain
3) Apply PARA placement rule
4) Apply Muse + Enneagram tags
5) Cross-link to relevant MOCs/indices
6) Move file into PARA location
7) Update indices and tracking notes

## Non-Destructive Rules
- Preserve original filenames and extensions (unless a clear fix is needed).
- Do not edit binary files in place.
- Keep provenance notes where possible.
- Minimize changes to existing user edits.

## Why This Is Not Generic Cleanup
The vault is an evolving knowledge system:
- Tagging is a semantic layer for pattern recognition and system evolution.
- Indexing is the navigation spine for cross-domain synthesis.
- Muse + Enneagram overlay is a primary organizing dimension, not a post-hoc label.
