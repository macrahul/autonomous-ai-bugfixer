def apply_safe_fix(file_path: str) -> bool:
    """
    Idempotent safe fix for ZeroDivisionError in divide().
    Returns:
      True  -> fix was applied
      False -> fix already present OR not applicable
    """
    with open(file_path, "r") as f:
        content = f.read()

    # ✅ Fix already exists → NO-OP
    if "if b == 0:" in content:
        print("ℹ️ Safe fix already present. Skipping.")
        return False

    lines = content.splitlines(keepends=True)

    new_lines = []
    inside_divide = False
    fixed = False

    for line in lines:
        if line.startswith("def divide"):
            inside_divide = True
            new_lines.append(line)
            continue

        if inside_divide and line.strip() == "return a / b":
            new_lines.append("    if b == 0:\n")
            new_lines.append("        return 'Error: Division by zero'\n")
            new_lines.append("    return a / b\n")
            inside_divide = False
            fixed = True
            continue

        new_lines.append(line)

    if not fixed:
        print("ℹ️ No applicable change found.")
        return False

    with open(file_path, "w") as f:
        f.writelines(new_lines)

    return True