import os
from github import Github

def get_repo_tree(repo_name):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(repo_name)

    contents = repo.get_contents("")
    paths = []

    while contents:
        item = contents.pop(0)
        if item.type == "dir":
            contents.extend(repo.get_contents(item.path))
        else:
            paths.append(item.path)

    return paths