def build_prompt(repo_path: str, user_query: str, file_list: list[str], file_samples: dict, search_results: list[str]) -> str:
    files_str = "\n".join(file_list[:20])
    samples_str = ""
    for fname, content in file_samples.items():
        samples_str += f"\n--- {fname} ---\n{content[:600]}\n"
    search_str = "\n".join(search_results[:8]) if search_results else "No results."

    return f"""You are a code analysis assistant. Analyze this repository and answer the user's query.

REPO PATH: {repo_path}
USER QUERY: {user_query}

FILE LIST (first 20):
{files_str}

KEY FILE CONTENTS:
{samples_str}

SEARCH RESULTS FOR QUERY KEYWORDS:
{search_str}

Return ONLY valid JSON in this exact format, no explanation, no markdown:
{{
  "repo_summary": "one sentence describing the repo",
  "what_it_does": "2-3 sentences on purpose and functionality",
  "key_files": ["list of 3-5 most important files"],
  "insights": ["2-4 insights relevant to the user query"],
  "risks": ["1-3 potential issues or concerns, or empty list if none"],
  "suggested_actions": ["1-3 concrete next steps for the user"]
}}"""
