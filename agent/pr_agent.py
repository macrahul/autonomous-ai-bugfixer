from github import Github
import os

def create_pr(repo_name, branch, file_path, content, sha):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(repo_name)

    repo.update_file(
        path=file_path,
        message="Autonomous AI: bug fix",
        content=content,
        sha=sha,
        branch=branch
    )

    repo.create_pull(
        title="Autonomous AI Fix",
        body="Root cause, fix, and validation done by AI agent.",
        head=branch,
        base="main"
    )