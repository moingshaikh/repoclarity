# RepoClarity

**Understand any local repo, clearly.**

RepoClarity is a local-first CLI tool that helps developers quickly understand a codebase using a local LLM.

No API keys. No cloud. No data leaving your machine.

---

## The problem

Opening a new repo is slow.

- README is incomplete  
- Codebase is unfamiliar  
- You don’t know where to start  

You spend 20–30 minutes just figuring out:
- what this repo does  
- which files matter  
- whether it’s worth your time  

---

## What RepoClarity does

RepoClarity analyzes a repository locally and returns a structured breakdown:

- what the repo does  
- key files to look at  
- important insights  
- risks or limitations  
- suggested next steps  

All in one response.

---

## Example

```bash
rclr ./some-repo "what does this repo do and what are the risks"
```

Output:

```json
{
  "repo_summary": "...",
  "key_files": [...],
  "insights": [...],
  "risks": [...],
  "suggested_actions": [...]
}
```

---

## Why local-first matters

- no API costs  
- no rate limits  
- works offline  
- safe for private codebases  

---

## How it works

- scans key files in the repo  
- builds a constrained context  
- sends it to a local LLM (via Ollama)  
- returns structured output  

---

## Requirements

- Python 3.12+
- Ollama installed
- Model:
  ```bash
  ollama pull qwen2.5-coder
  ```

---

## Install

```bash
git clone https://github.com/moingshaikh/repoclarity.git
cd repoclarity
pip install -e .
```

---

## Usage

```bash
rclr ./repo "what does this repo do"
```

---

## Scope (v1)

RepoClarity v1 focuses on:

- fast repo understanding  
- local execution  
- structured output  

Not included yet:

- deep code analysis  
- multi-file reasoning chains  
- agent workflows  

---

## Why this exists

Most AI tooling today assumes:

- cloud access  
- API keys  
- external inference  

RepoClarity explores a different direction:

> **What if understanding codebases could happen entirely locally?**

---

## License

MIT
