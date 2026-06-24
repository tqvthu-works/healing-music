# Healing Music Prompt Generator

AI music prompt generator (Suno/Udio) for healing music, lofi, ambient, nature soundscape, sleep music, meditation music.

## Structure

- **`HEALING-MUSIC.md`** — Defines 12 healing music categories, instruments, mood tags, keywords & templates for each genre.
- **`AGENT.md`** — System prompt for AI Agent, guides mix & match, high variance rule, output format (Style of Music + Meta-tags).
- **`.agents/skills/healing-music-prompt/SKILL.md`** — OpenCode skill to auto-activate the agent.

## Usage

### Method 1: Use directly with AI Agent

Once the Agent has read both `HEALING-MUSIC.md` and `AGENT.md`, you can chat with very short prompts like:

- *"Give me a Nature Hybrid prompt"*
- *"Create a Lofi Healing track focused on nighttime rain"*
- *"Create a Sleep Music prompt with Udio"*

The Agent will automatically think, randomly select instruments and nature elements (rain, streams, birdsong...), and mix a completely new, precise prompt set (Style + Meta-tags) aligned with AI prompting techniques!

### Method 2: Use OpenCode Skill

If using OpenCode, load this skill with the command:

```
/healing-music-prompt 
```

Then chat directly requesting a prompt. The skill will automatically activate AGENT.md + HEALING-MUSIC.md as the knowledge base and handle all requests.
