def apply_fix():
    with open("repo_clone/app.py", "r") as f:
        code = f.read()

    fixed_code = code.replace(
        "return a / b",
        "return a / b if b != 0 else 0"
    )

    with open("repo_clone/app.py", "w") as f:
        f.write(fixed_code)