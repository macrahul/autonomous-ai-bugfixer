from agent.triage import is_fixable
from agent.planner import create_plan
from agent.registry import select_executor
from agent.reflection import should_retry
from agent.log_parser import parse_error_blocks

from core.git_ops import create_branch, commit_all, push_branch
from agent.pr_agent import create_pr
from agent.pr_agent import pr_exists

import subprocess
import datetime
import sys

REPO_NAME = "macrahul/autonomous-ai-bugfixer"
MAX_RETRIES = 1

# ---------------------------
# 1. Read production error
# ---------------------------
with open("inputs/prod_error.log") as f:
    error_log = f.read()

if not is_fixable(error_log):
    sys.exit("Not fixable by AI")

# ---------------------------
# 2. Parse log into individual errors
# ---------------------------
error_blocks = parse_error_blocks(error_log)

if not error_blocks:
    sys.exit("No valid traceback blocks found.")

# ---------------------------
# 3. Process each error independently
# ---------------------------
for error_block, file_path in error_blocks:

    print("\n====================================")
    print(f"🚨 Processing error for: {file_path}")
    print("====================================")

    # ✅ Generate plan ONLY for this error
    plan = create_plan(error_block)
    print("✅ PLAN:", plan)

    if not file_path.startswith("repo_clone/"):
        print("⚠ Skipping non-project file")
        continue

    local_path = file_path

    # ✅ Reset to clean main
    subprocess.run(["git", "checkout", "main"])
    subprocess.run(["git", "reset", "--hard"])

    attempt = 0
    fix_applied = False

    # ---------------------------
    # Apply fix with retry
    # ---------------------------
    while True:
        executor = select_executor(error_block)

        if not executor:
            print("❌ No executor found for this error.")
            break

        print(f"🧠 Selected Executor: {executor.name()}")

        if executor.name() == "AIExecutor":
            applied = executor.apply_fix(local_path, error_block)
        else:
            applied = executor.apply_fix(local_path)

        if applied:
            fix_applied = True
            print("✅ SAFE FIX APPLIED")
        else:
            print("ℹ️ No fix needed or already present")

        print("🔍 VERIFYING FIX...")
        result = subprocess.run(
            ["python", local_path],
            capture_output=True,
            text=True
        )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode == 0:
            print("✅ VERIFICATION PASSED")
            break

        attempt += 1

        if not should_retry(attempt, MAX_RETRIES):  # [2]
            print("❌ Fix failed after retries")
            break

        print("🔁 Retrying fix attempt...")

    # ---------------------------
    # Create PR only if fix applied
    # ---------------------------
    if fix_applied:

        pr_title = f"Autonomous AI Fix for {file_path}"

        # ✅ Check PR existence AFTER fix
        if pr_exists(REPO_NAME, pr_title):
            print("ℹ️ PR already exists. Skipping branch creation.")
        else:
            branch = f"ai-fix-{file_path.replace('/', '-').replace('.py', '')}"
            print("🌿 CREATING BRANCH:", branch)

            create_branch(branch)

            committed = commit_all(f"Autonomous AI fix for {file_path}")

            if committed:
                print("🚀 PUSHING BRANCH")
                push_branch(branch)

                print("🔀 CREATING PR")
                create_pr(
                    repo_name=REPO_NAME,
                    branch=branch,
                    title=pr_title,
                    body=f"""
### 🤖 Autonomous AI Fix

**File**
{file_path}

**Plan**
{plan}
"""
                )

                print("✅ PR CREATED")

    # ✅ Return to clean main
    subprocess.run(["git", "checkout", "main"])
    subprocess.run(["git", "reset", "--hard"])

print("\n✅ MULTI-ERROR PROCESSING COMPLETED")