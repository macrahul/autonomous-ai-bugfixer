from .base import BaseExecutor

class ZeroDivisionExecutor(BaseExecutor):

    def name(self) -> str:
        return "ZeroDivisionExecutor"

    def applies_to(self, error_log: str) -> bool:
        return "ZeroDivisionError" in error_log

    def apply_fix(self, file_path: str) -> bool:
        with open(file_path, "r") as f:
            content = f.read()

        # Idempotency check
        if "if b == 0:" in content:
            return False

        if "return a / b" not in content:
            return False

        fixed_content = content.replace(
            "return a / b",
            "if b == 0:\n        return 'Error: Division by zero'\n    return a / b"
        )

        with open(file_path, "w") as f:
            f.write(fixed_content)

        return True