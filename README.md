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

## Tools

### `metadata-tagger.py`

Batch tag MP3 files with metadata (artist, album, title, genre, etc.) using ffmpeg.

```bash
# Tag a single file
python metadata-tagger.py -i input.mp3 --artist "Name" --title "Song"

# Batch tag all MP3s in a directory
python metadata-tagger.py -i ./music/ --album "My Album" --year 2026

# Force overwrite existing output files
python metadata-tagger.py -i input.mp3 --artist "Name" --overwrite
python metadata-tagger.py -i input.mp3 --artist "Name" --force

# Preview without writing
python metadata-tagger.py -i input.mp3 --artist "Name" --dry-run
```

Config is stored in `config.json` (auto-created with defaults). CLI flags take precedence over config values.

### `show-metadata.py`

Display MP3 metadata and technical info using mutagen.

```bash
# Show metadata for one file
python show-metadata.py file.mp3

# Show metadata for multiple files
python show-metadata.py *.mp3

# JSON output
python show-metadata.py file.mp3 --json
```

Displays ID3 tags (title, artist, album, year, genre, track, disc, composer, comment, cover art) and audio info (duration, bitrate, sample rate, channels).
