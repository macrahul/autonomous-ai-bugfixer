import subprocess

def _run(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        if "nothing to commit" in result.stderr.lower():
            return result.stdout.strip()
        raise RuntimeError(result.stderr)
    return result.stdout.strip()

def create_branch(branch_name: str):
    _run(["git", "checkout", "-b", branch_name])

def commit_all(message: str) -> bool:
    """
    Commits changes if any exist.
    Returns True if a commit was created, False if no changes.
    """
    status = _run(["git", "status", "--porcelain"])
    if not status.strip():
        print("ℹ️ No changes to commit. Skipping commit.")
        return False

    _run(["git", "add", "."])
    _run(["git", "commit", "-m", message])
    return True

def push_branch(branch_name: str):
    _run(["git", "push", "-u", "origin", branch_name])