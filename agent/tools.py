from github import Github
import os

def create_pr():
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo("macrahul/autonomous-ai-bugfixer")

    base_branch = "main"
    new_branch = "ai-fix-zero-div"
    file_path = "repo_clone/app.py"   # ✅ FIXED PATH

    base = repo.get_branch(base_branch)

    # Create new branch
    try:
        repo.create_git_ref(
            ref=f"refs/heads/{new_branch}",
            sha=base.commit.sha
        )
    except:
        pass  # branch already exists

    contents = repo.get_contents(file_path, ref=new_branch)

    repo.update_file(
        path=file_path,
        message="AI Agent: Fix ZeroDivisionError",
        content=open("repo_clone/app.py").read(),
        sha=contents.sha,
        branch=new_branch
    )

    repo.create_pull(
        title="AI Agent Fix: Prevent division by zero",
        body="Autonomous AI agent detected production error, fixed code, and self-verified.",
        head=new_branch,
        base=base_branch
    )