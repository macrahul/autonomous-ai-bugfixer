from openai import OpenAI
client = OpenAI()

def generate_patch(file_path, code, error_log):
    prompt = f"""
    You are fixing {file_path}.
    Error:
    {error_log}

    Rules:
    - Minimal changes
    - No new dependencies
    - Return unified diff ONLY

    Code:
    {code}
    """
    res = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return res.output_text

def generate_diff(file_path: str, code: str, error_log: str) -> str:
    prompt = f"""
You are an autonomous software engineer.

FILE: {file_path}

ERROR:
{error_log}

RULES:
- Fix the error
- Change minimal lines
- Do NOT add new dependencies
- Return UNIFIED DIFF ONLY
- No explanations
- No markdown fences

CODE:
{code}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text