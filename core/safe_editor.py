def apply_safe_fix(file_path: str) -> bool:
    """
    Safely edits the divide() function to prevent division by zero.
    Deterministic and idempotent.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    inside_divide = False
    fixed = False

    for line in lines:
        if line.startswith("def divide"):
            inside_divide = True
            new_lines.append(line)
            continue

        if inside_divide and "return a / b" in line:
            new_lines.append("    if b == 0:\n")
            new_lines.append("        return 'Error: Division by zero'\n")
            new_lines.append("    return a / b\n")
            inside_divide = False
            fixed = True
            continue

        new_lines.append(line)

    if not fixed:
        print("❌ Safe editor: no change applied")
        return False

    with open(file_path, "w") as f:
        f.writelines(new_lines)

    return True