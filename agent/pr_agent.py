from github import Github
import os

def create_pr(repo_name, branch, title, body):
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