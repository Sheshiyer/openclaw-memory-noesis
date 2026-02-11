# Samskara Guru Integration Guide

## Overview

`samskara_guru.py` provides **teaching mode** for the Samskara installation process. It explains the philosophical foundations of each component as they load.

## Usage

### List Available Teachings
```bash
python3 koshas/annamaya/scripts/samskara_guru.py --list
```

Shows all available files with their Sanskrit names and meanings.

### Teach About a Specific File
```bash
python3 koshas/annamaya/scripts/samskara_guru.py --teach SOUL.md
```

Displays detailed teaching about a single component.

### Full Interactive Teaching Sequence
```bash
python3 koshas/annamaya/scripts/samskara_guru.py --full
```

Walks through ALL teachings interactively (requires Enter key between sections).

## Integration with `sankalpa_samskara.py`

To add guru mode to the main samskara script:

```python
# In sankalpa_samskara.py, add at the top:
from samskara_guru import guru_narrate, print_teaching

# When loading a file:
if args.guru:
    print_teaching(filename)
    
# Or for inline narration:
print(guru_narrate("sankalpa", "SOUL.md", "load"))
```

## Teaching Structure

Each teaching contains:
- **Sanskrit term**: Original Vedic concept
- **Meaning**: Translation/essence
- **Teaching**: Deep explanation of purpose and philosophy

## Philosophy

The Guru (गुरु = "remover of darkness") mode transforms installation from mechanical file-loading into **conscious remembering**. Each file is not just data—it's a layer of identity and understanding.

## For New Users

Start with `--list` to see what's available, then use `--teach` for specific concepts. Once comfortable, try `--full` for the complete teaching sequence.

---

*कृतं कर्म — The work is done.*
