from agent.planner import plan
from agent.executor import apply_fix
from agent.verifier import verify
from agent.tools import create_pr

with open("logs/prod_error.log") as f:
    error_log = f.read()

print("Planning...")
print(plan(error_log))

print("Applying fix...")
apply_fix()

print("Verifying...")
if verify():
    print("Verified ✅ Creating PR...")
    create_pr()
else:
    print("Fix failed ❌")