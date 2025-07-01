from typing import Annotated
from langchain.tools import tool
from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

github = Github(os.getenv("GITHUB_ACCESS_TOKEN"))


@tool
async def get_pull_requests(
    repo_name: Annotated[str, "github repository name"],
    state: Annotated[str, "pull request state"] = "open",
) -> str:
    """Use this tool for github. Get pull requests from a repository."""

    repo = github.get_repo(repo_name)
    return repo.get_pulls(state=state)


@tool
async def get_pull_request_changed_files(
    repo_name: Annotated[str, "github repository name"],
    pull_request_number: Annotated[int, "pull request number"],
) -> str:
    """Use this tool for github. Get detailed file changes from a pull request including code changes."""
    repo = github.get_repo(repo_name)
    pr = repo.get_pull(pull_request_number)

    files = pr.get_files()

    result = []
    for file in files:
        file_info = {
            "filename": file.filename,
            "status": file.status,  # added, modified, removed
            "additions": file.additions,
            "deletions": file.deletions,
            "changes": file.changes,
            "patch": file.patch,  # 실제 코드 변경 내용
            "raw_url": file.raw_url,
            "blob_url": file.blob_url,
        }
        result.append(file_info)

    return result
