from agent.triage import is_fixable
from agent.planner import create_plan
from agent.file_finder import find_files
from agent.patch_generator import generate_patch
from agent.pr_agent import create_pr
from core.repo_manager import get_repo_tree
from core.sandbox import run_checks
from core.config import MAX_RETRIES

with open("inputs/prod_error.log") as f:
    error_log = f.read()

if not is_fixable(error_log):
    exit("Not fixable by AI")

plan = create_plan(error_log)
repo_tree = get_repo_tree("macrahul/autonomous-ai-bugfixer")
files = find_files(error_log, repo_tree)

attempt = 0
valid_files = []

for file in files:
    if file.startswith("repo_clone/") and file.endswith(".py"):
        valid_files.append(file.replace("repo_clone/", ""))

if not valid_files:
    exit("No valid files found to fix")

for file in valid_files:
    with open(f"repo_clone/{file}") as f:
        code = f.read()