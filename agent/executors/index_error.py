from .base import BaseExecutor

class IndexErrorExecutor(BaseExecutor):

    def name(self) -> str:
        return "IndexErrorExecutor"

    def applies_to(self, error_log: str) -> bool:
        return "IndexError" in error_log

    def apply_fix(self, file_path: str) -> bool:
        with open(file_path, "r") as f:
            content = f.read()

        # Simple guard for list indexing
        if "IndexError" not in content and "[" not in content:
            return False

        # Minimal safe strategy example
        if "if len(" in content:
            return False  # Already guarded

        lines = content.splitlines(keepends=True)
        new_lines = []
        applied = False

        for line in lines:
            if "[" in line and "]" in line and "=" not in line:
                indent = " " * (len(line) - len(line.lstrip()))
                new_lines.append(f"{indent}if len({line.strip().split('[')[0]}) > 0:\n")
                new_lines.append(f"{indent}    {line}")
                applied = True
            else:
                new_lines.append(line)

        if not applied:
            return False

        with open(file_path, "w") as f:
            f.writelines(new_lines)

        return True