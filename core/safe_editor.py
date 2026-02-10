def apply_safe_fix(file_path: str) -> bool:
    """
    Idempotent safe fix for ZeroDivisionError in divide().
    Will NOT apply the fix if it already exists.
    """
    with open(file_path, "r") as f:
        content = f.read()

    # ✅ IDENTITY CHECK (CRITICAL)
    if "if b == 0:" in content:
        print("ℹ️ Safe fix already present. Skipping.")
        return True

    lines = content.splitlines(keepends=True)

    new_lines = []
    inside_divide = False
    fixed = False

    for line in lines:
        new_lines.append(line)

        if line.startswith("def divide"):
            inside_divide = True
            continue

        if inside_divide and line.strip() == "return a / b":
            # Remove the last appended return
            new_lines.pop()

            new_lines.append("    if b == 0:\n")
            new_lines.append("        return 'Error: Division by zero'\n")
            new_lines.append("    return a / b\n")

            inside_divide = False
            fixed = True

    if not fixed:
        print("❌ Safe editor: no applicable change found")
        return False

    with open(file_path, "w") as f:
        f.writelines(new_lines)

    return True