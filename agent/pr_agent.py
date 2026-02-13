from github import Github
import os

def create_pr(repo_name: str, branch: str, title: str, body: str):
    """
    Creates a GitHub Pull Request from branch -> main
    Prevents duplicate PR creation.
    """

    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(repo_name)

    # ✅ 1. Check for existing open PRs
    open_prs = repo.get_pulls(state="open")

    for pr in open_prs:
        if pr.head.ref == branch:
            print("ℹ️ PR already exists for this branch. Skipping.")
            return pr.html_url

        if pr.title.strip() == title.strip():
            print("ℹ️ PR with same title already exists. Skipping.")
            return pr.html_url

    # ✅ 2. Create new PR if none exists
    pr = repo.create_pull(
        title=title,
        body=body,
        head=branch,
        base="main"
    )

    print("✅ PR CREATED:", pr.html_url)
    return pr.html_url