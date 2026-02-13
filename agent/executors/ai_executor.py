from openai import OpenAI

class AIExecutor:

    def name(self):
        return "AIExecutor"

    def applies_to(self, error_log):
        return True  # fallback

    def apply_fix(self, file_path):
        client = OpenAI()

        with open(file_path, "r") as f:
            code = f.read()

        prompt = f"""
        Fix the following Python code based on this error:
        ERROR:
        {error_log}

        CODE:
        {code}

        Return only corrected code.
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        fixed_code = response.output_text

        with open(file_path, "w") as f:
            f.write(fixed_code)

        return True