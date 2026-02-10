from agent.triage import is_fixable
from agent.planner import create_plan
from agent.file_finder import find_files
from core.repo_manager import get_repo_tree
from agent.patch_generator import generate_diff
from core.safe_editor import apply_safe_fix
import subprocess

with open("inputs/prod_error.log") as f:
    error_log = f.read()

if not is_fixable(error_log):
    exit("Not fixable by AI")

plan = create_plan(error_log)
print("✅ PLAN:", plan)

repo_tree = get_repo_tree("macrahul/autonomous-ai-bugfixer")
files = find_files(error_log, repo_tree)

valid_files = []

for file in files:
    if file.endswith(".py"):
        if file.startswith("repo_clone/"):
            valid_files.append(file.replace("repo_clone/", ""))
        else:
            valid_files.append(file)

print("✅ VALID FILES:", valid_files)

if not valid_files:
    exit("No valid files found to fix")

for file in valid_files:
    local_path = f"repo_clone/{file}"

    print("✅ OPENING FILE:", local_path)
    with open(local_path) as f:
        code = f.read()

    diff = generate_diff(file, code, error_log)

    print("\n🧩 GENERATED DIFF:")
    print(diff)

    print("🛠️ APPLYING SAFE FIX...")
    success = apply_safe_fix(local_path)

    if not success:
        exit("Safe fix application failed")

    print("✅ SAFE FIX APPLIED")

    print("🔍 VERIFYING FIX...")
    result = subprocess.run(
        ["python", local_path],
        capture_output=True,
        text=True
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if result.returncode != 0:
        exit("❌ Verification failed")

    print("✅ VERIFICATION PASSED")

    if not success:
        exit("Patch application failed")

    print("✅ DIFF APPLIED SUCCESSFULLY")