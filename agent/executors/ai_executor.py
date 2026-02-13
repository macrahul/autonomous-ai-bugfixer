from openai import OpenAI
import re

class AIExecutor:

    def name(self):
        return "AIExecutor"

    def applies_to(self, error_log: str) -> bool:
        return True  # Always fallback

    def apply_fix(self, file_path: str, error_log: str) -> bool:
        client = OpenAI()

        with open(file_path, "r") as f:
            code = f.read()

        prompt = f"""
Fix the following Python code based on this error.

Return ONLY valid Python code.
Do NOT include markdown fences.
Do NOT include explanations.

ERROR:
{error_log}

CODE:
{code}
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        fixed_code = response.output_text.strip()

        # ✅ Remove markdown code fences if present
        fixed_code = re.sub(r"^```.*?\n", "", fixed_code)
        fixed_code = re.sub(r"\n```$", "", fixed_code)

        if not fixed_code:
            return False

        with open(file_path, "w") as f:
            f.write(fixed_code)

        return True