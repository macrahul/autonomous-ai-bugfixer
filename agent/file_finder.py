from openai import OpenAI
import json

client = OpenAI()

def find_files(error_log, repo_tree):
    prompt = f"""
You are an autonomous code analysis agent.

Given:
ERROR:
{error_log}

REPO_FILES:
{repo_tree}

Return STRICT JSON only in this format:
{{
  "files": ["relative/path/file.py"]
}}

Rules:
- Only include files from REPO_FILES
- Prefer files mentioned in stack traces
- Return empty list if no match
- No explanations
- STRICT JSON only
"""

    res = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    try:
        data = json.loads(res.output_text)
        return data.get("files", [])
    except Exception:
        return []