from openai import OpenAI
client = OpenAI()

def plan(error_log):
    prompt = f"""
    You are an autonomous software engineer.
    Analyze the error and decide steps to fix it.

    Error:
    {error_log}

    Return steps as bullet points.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content