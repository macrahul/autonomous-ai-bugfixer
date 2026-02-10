from github import Github
import os

def create_pr():
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo("rahul-gupta/autonomous-ai-bugfixer")

    base = repo.get_branch("main")
    repo.create_git_ref(
        ref="refs/heads/ai-fix-zero-div",
        sha=base.commit.sha
    )

    repo.update_file(
        "app.py",
        "AI Agent: Fix ZeroDivisionError",
        open("repo_clone/app.py").read(),
        repo.get_contents("app.py").sha,
        branch="ai-fix-zero-div"
    )

    repo.create_pull(
        title="AI Agent Fix: Prevent division by zero",
        body="Autonomous AI agent detected error and fixed it.",
        head="ai-fix-zero-div",
        base="main"
    )