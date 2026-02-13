from .base import BaseExecutor

class IndexErrorExecutor(BaseExecutor):

    def name(self) -> str:
        return "IndexErrorExecutor"

    def applies_to(self, error_log: str) -> bool:
        return "IndexError" in error_log

    def apply_fix(self, file_path: str) -> bool:
        with open(file_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        applied = False

        for line in lines:
            stripped = line.strip()

            # Match: return items[0]
            if stripped.startswith("return") and "[" in stripped and "]" in stripped:
                indent = line[:len(line) - len(line.lstrip())]

                # Extract variable safely
                # Example: return items[0]
                variable_part = stripped.replace("return", "").strip()
                variable_name = variable_part.split("[")[0].strip()

                new_lines.append(f"{indent}if len({variable_name}) > 0:\n")
                new_lines.append(f"{indent}    return {variable_name}[0]\n")
                new_lines.append(f"{indent}else:\n")
                new_lines.append(f"{indent}    return None\n")

                applied = True
            else:
                new_lines.append(line)

        if not applied:
            return False

        with open(file_path, "w") as f:
            f.writelines(new_lines)

        return True