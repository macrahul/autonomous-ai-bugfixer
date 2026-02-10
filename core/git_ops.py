import subprocess

def _run(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()

def create_branch(branch_name: str):
    _run(["git", "checkout", "-b", branch_name])

def commit_all(message: str):
    _run(["git", "add", "."])
    _run(["git", "commit", "-m", message])

def push_branch(branch_name: str):
    _run(["git", "push", "-u", "origin", branch_name])