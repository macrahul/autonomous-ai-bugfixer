import subprocess

def run_checks():
    cmds = [["python", "app.py"]]
    for cmd in cmds:
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode != 0:
            return False
    return True