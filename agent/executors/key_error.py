from .base import BaseExecutor

class KeyErrorExecutor(BaseExecutor):

    def name(self) -> str:
        return "KeyErrorExecutor"

    def applies_to(self, error_log: str) -> bool:
        return "KeyError" in error_log

    def apply_fix(self, file_path: str) -> bool:
        with open(file_path, "r") as f:
            content = f.read()

        if ".get(" in content:
            return False  # Already safe

        if "[" not in content:
            return False

        lines = content.splitlines(keepends=True)
        new_lines = []
        applied = False

        for line in lines:
            if "[" in line and "]" in line and "=" not in line:
                # Convert dict[key] → dict.get(key)
                left = line.split("[")[0]
                key = line.split("[")[1].split("]")[0]
                indent = " " * (len(line) - len(line.lstrip()))
                new_lines.append(f"{indent}{left}.get({key})\n")
                applied = True
            else:
                new_lines.append(line)

        if not applied:
            return False

        with open(file_path, "w") as f:
            f.writelines(new_lines)

        return True