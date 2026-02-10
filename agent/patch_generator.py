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