# repoclarity

**Understand any repo, locally.**

A local-first CLI tool that helps developers quickly understand a codebase using a local LLM. No API keys. No cloud. Just clarity.

---

## Requirements

- Python 3.12+
- [Ollama](https://ollama.com) installed and running
- `qwen2.5-coder` model pulled locally

```bash
ollama pull qwen2.5-coder
```

---

## Installation

```bash
git clone https://github.com/yourusername/repoclarity.git
cd repoclarity
pip install -e .
```

This registers two CLI commands: `rclr` and `repoclarity`.

---

## Usage

```bash
rclr ./path/to/repo "your question or intent"
```

Or:

```bash
repoclarity ./path/to/repo "find potential issues"
```

---

## Example

```bash
rclr ./myproject "what does this repo do and what are the risks"
```

**Example output:**

```json
{
  "repo_summary": "A Flask-based REST API for managing user authentication.",
  "what_it_does": "Provides JWT-based login and registration endpoints. Uses SQLite for local development and PostgreSQL in production.",
  "key_files": ["main.py", "auth/routes.py", "requirements.txt", "README.md"],
  "insights": [
    "Authentication logic is centralized in auth/routes.py",
    "Environment variables are used for secrets but no .env.example is present"
  ],
  "risks": [
    "No rate limiting on login endpoint",
    "SQLite used in dev may mask production-only bugs"
  ],
  "suggested_actions": [
    "Add .env.example for onboarding clarity",
    "Review auth/routes.py for input validation",
    "Test against PostgreSQL locally before deploying"
  ]
}
```

---

## How it works

1. Lists all files in the repo
2. Reads key files (README, entry points, config)
3. Searches code for keywords from your query
4. Passes context to `qwen2.5-coder` via Ollama
5. Returns structured JSON insights

All processing happens on your machine.

---

## Notes

- Performance depends on your hardware. Apple Silicon and GPU machines will respond in seconds. CPU-only machines will take longer.
- Output quality depends on README and code clarity in the target repo.
- v1 is intentionally minimal, understand first, extend later.

---

Built by [Moin Shaikh](https://www.linkedin.com/in/moingshaikh/)
