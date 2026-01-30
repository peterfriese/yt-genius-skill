# YouTube Genius Skill

This project provides a specialized skill for AI agents (like Gemini and Antigravity) to optimize YouTube content. It automates fetching transcripts, generating SEO-optimized metadata, creating accurate timestamped chapters, and drafting social media posts.

## Core Capabilities
- **Transcript Extraction**: Uses `scripts/get_transcript.py` to fetch video transcripts in a compact, token-efficient format.
- **Metadata Generation**: Creates high-CTR titles, SEO descriptions, and hashtags.
- **Precision Chapters**: Follows a strict workflow to map transcript segments to exact timestamps.
- **Social Media Repurposing**: Drafts platform-specific copy for Twitter, LinkedIn, and more.
- **Twitter Articles**: Converts transcripts into structured, long-form articles with embedded clip markers and hero image concepts.

## AI Instructions & Rules

### Working with Transcripts
- Always use the bundled `scripts/get_transcript.py` for YouTube URLs.
- Prefer the compact text output over verbose JSON to maximize context window efficiency.
- **Chapter Rule**: NEVER hallucinate or shift timestamps. They must match the transcript segments exactly.

### Project Structure
- `.gemini/skills/yt-genius/`: Contains the main `SKILL.md` and helper scripts.
- `scripts/`: Python utilities for data fetching. Use the virtual environment in `.venv/` if available.
- `GEMINI.md`: This file—serves as the source of truth for AI agent behavior in this repo.

### Git Hygiene
- Do not commit `.txt` logs or transcript snapshots.
- Ensure `requirements.txt` is updated if new dependencies are added to the fetch scripts.
