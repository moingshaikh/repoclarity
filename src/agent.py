import json
import requests
from pathlib import Path
from .tools import list_files, read_file, search_code
from .prompts import build_prompt

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder"

KEY_FILE_NAMES = {
    "readme", "readme.md", "readme.txt", "main.py", "app.py", "index.py",
    "index.js", "index.ts", "main.js", "main.ts", "package.json",
    "pyproject.toml", "setup.py", "cargo.toml", "go.mod", "dockerfile",
    "docker-compose.yml", ".env.example"
}


def pick_key_files(file_list: list[str], max_files: int = 3) -> list[str]:
    """Pick the most informative files to read."""
    priority = []
    others = []
    for f in file_list:
        if Path(f).name.lower() in KEY_FILE_NAMES:
            priority.append(f)
        else:
            others.append(f)
    selected = priority[:max_files]
    if len(selected) < max_files:
        selected += others[:max_files - len(selected)]
    return selected


def extract_keywords(query: str) -> list[str]:
    """Simple keyword extraction from user query."""
    stopwords = {"find", "show", "list", "what", "how", "is", "are", "the", "a", "an", "in", "of", "for", "and", "or"}
    words = [w.strip(".,?!") for w in query.lower().split()]
    return [w for w in words if w not in stopwords and len(w) > 2][:3]


def call_ollama(prompt: str) -> str:
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1}
    }, timeout=900)
    return response.json()["response"]


def run_agent(repo_path: str, user_query: str) -> dict:
    repo = str(Path(repo_path).resolve())

    # Step 1: list files
    files = list_files(repo)
    if not files:
        return {"error": f"No files found in {repo_path}. Check the path."}

    # Step 2: read key files
    key_files = pick_key_files(files)
    file_samples = {}
    for f in key_files:
        file_samples[f] = read_file(repo, f)

    # Step 3: search for query keywords
    keywords = extract_keywords(user_query)
    search_results = []
    for kw in keywords:
        search_results += search_code(repo, kw)

    # Step 4: build prompt and call LLM
    prompt = build_prompt(repo_path, user_query, files, file_samples, search_results)
    raw = call_ollama(prompt)

    # Step 5: parse JSON
    try:
        clean = raw.strip()
        if "```" in clean:
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        return json.loads(clean.strip())
    except json.JSONDecodeError:
        return {"raw_output": raw, "parse_error": "Model did not return valid JSON. Raw output preserved."}
