from github import Github
import os

def pr_exists(repo_name: str, title: str):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(repo_name)

    open_prs = repo.get_pulls(state="open")

    for pr in open_prs:
        if pr.title.strip() == title.strip():
            return True

    return False


def create_pr(repo_name: str, branch: str, title: str, body: str):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(repo_name)

    pr = repo.create_pull(
        title=title,
        body=body,
        head=branch,
        base="main"
    )

    print("✅ PR CREATED:", pr.html_url)
    return pr.html_url