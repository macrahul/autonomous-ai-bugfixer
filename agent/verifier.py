import subprocess

def verify():
    result = subprocess.run(
        ["python", "repo_clone/app.py"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0