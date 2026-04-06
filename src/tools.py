import os
from pathlib import Path

IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build', '.idea', '.vscode'}
MAX_FILE_SIZE = 20_000  # characters


def list_files(repo_path: str) -> list[str]:
    """Recursively list all files in the repo, ignoring noise dirs."""
    results = []
    root = Path(repo_path)
    for path in sorted(root.rglob("*")):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.is_file():
            results.append(str(path.relative_to(root)))
    return results


def read_file(repo_path: str, file_path: str) -> str:
    """Read a file's contents. Truncates large files."""
    full_path = Path(repo_path) / file_path
    if not full_path.exists():
        return f"[File not found: {file_path}]"
    try:
        content = full_path.read_text(encoding="utf-8", errors="ignore")
        if len(content) > MAX_FILE_SIZE:
            content = content[:MAX_FILE_SIZE] + "\n\n[...truncated]"
        return content
    except Exception as e:
        return f"[Error reading file: {e}]"


def search_code(repo_path: str, keyword: str) -> list[str]:
    """Search for a keyword across all repo files. Returns matching lines with filenames."""
    results = []
    root = Path(repo_path)
    for path in sorted(root.rglob("*")):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        try:
            for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if keyword.lower() in line.lower():
                    rel = str(path.relative_to(root))
                    results.append(f"{rel}:{i}: {line.strip()}")
                    if len(results) >= 30:
                        return results
        except Exception:
            continue
    return results
