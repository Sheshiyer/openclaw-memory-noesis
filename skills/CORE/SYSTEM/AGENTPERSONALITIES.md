# Agent Voice Personalities

This file defines voice configurations for PAI agents. The Voice Server loads these configurations to provide consistent, personality-appropriate voices for different agent types.

## Voice Configuration Format

```json
{
  "voices": {
    "noesis": {
      "voice_id": "n7TYMDyW99AoiiVQVK83",
      "voice_name": "Pichet-noesis",
      "stability": 0.5,
      "similarity_boost": 0.75,
      "style": 0.0,
      "speed": 1.0,
      "use_speaker_boost": true,
      "description": "Secondary PAI voice. A warm, grounded male voice in his mid-30s with a slight British accent. Thoughtful and measured, never rushed. Perfect for teaching, explanations, and complex topics.",
      "type": "secondary",
      "prosody": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.0,
        "speed": 1.0,
        "use_speaker_boost": true,
        "volume": 1.0
      }
    },
    "pattern-seer": {
      "voice_id": "wW2ZEfGw0PrbOIg4GVDH",
      "voice_name": "Pattern-Seer",
      "stability": 0.5,
      "similarity_boost": 0.75,
      "style": 0.0,
      "speed": 1.25,
      "use_speaker_boost": false,
      "description": "Default PAI voice. A woman in her 30s to early 40s with a thick British accent. Excited and candid, like talking to a friend. Perfect for discoveries, insights, patterns, and research findings.",
      "type": "primary",
      "prosody": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.0,
        "speed": 1.25,
        "use_speaker_boost": false,
        "volume": 1.0
      }
    },
    "observer-integrator": {
      "voice_id": "8V5TtIiGKsYlj2MIm9dt",
      "voice_name": "Observer-Integrator",
      "stability": 0.5,
      "similarity_boost": 0.75,
      "style": 0.0,
      "speed": 1.0,
      "use_speaker_boost": true,
      "description": "Completion and status voice. A warm, grounded male voice in his mid-30s with a slight British accent. Rich and resonant with clear midrange depth. Perfect for completions, status updates, summaries, and integration tasks.",
      "type": "completion",
      "prosody": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.0,
        "speed": 1.0,
        "use_speaker_boost": true,
        "volume": 1.0
      }
    }
  }
}
```

## Voice Selection Guidelines

### Pattern-Seer (Primary - Default)
**Use for:**
- General PAI responses (default voice)
- Research findings and discoveries
- Pattern identification
- Data analysis results
- Insight generation
- Exploration and investigation results
- Default fallback

**Tone:** Excited, energetic, like sharing discoveries with a friend

### Pichet-noesis (Secondary)
**Use for:**
- Teaching and explanations
- Complex technical topics
- Problem-solving discussions

**Tone:** Thoughtful, measured, patient teacher

### Observer-Integrator (Completion)
**Use for:**
- Task completions
- Status updates
- Progress summaries
- Integration confirmations
- Build/deployment results
- System state reports

**Tone:** Warm, grounded, resonant authority

## Default Voice

The default voice for noesisX is **pattern-seer** (`wW2ZEfGw0PrbOIg4GVDH`).

This is configured via `ELEVENLABS_VOICE_ID` in `settings.json` env and read by `identity.ts`.
