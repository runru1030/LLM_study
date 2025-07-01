from typing import Annotated
from langchain.tools import tool
from github import Github
from dotenv import load_dotenv
import os

load_dotenv()


class GitHubClient:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            token = os.getenv("GITHUB_ACCESS_TOKEN")
            if not token:
                raise ValueError("GITHUB_ACCESS_TOKEN이 설정되지 않았습니다.")
            self._client = Github(token)
        return self._client

    def get_repo(self, repo_name: str, org_name: str | None = None):
        if org_name:
            org = self.client.get_organization(org_name)
            return org.get_repo(repo_name)
        else:
            return self.client.get_repo(repo_name)


github_client = GitHubClient()


@tool
async def get_pull_requests(
    repo_name: Annotated[str, "github repository name"],
    state: Annotated[str, "pull request state"] = "open",
    org_name: Annotated[str | None, "github organization name"] = None,
) -> str:
    """Use this tool for github. Get pull requests from a repository."""
    try:
        repo = github_client.get_repo(repo_name, org_name)
        pulls = repo.get_pulls(state=state)

        result = []
        for pr in pulls:
            pr_info = {
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "author": pr.user.login,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "url": pr.html_url,
                "body": pr.body[:200] + "..."
                if pr.body and len(pr.body) > 200
                else pr.body,
            }
            result.append(pr_info)

        return f"총 {len(result)}개의 {state} Pull Request를 찾았습니다: {result}"

    except Exception as e:
        return f"Pull Request 조회 실패: {str(e)}"


@tool
async def get_pull_request_changed_files(
    repo_name: Annotated[str, "github repository name"],
    pull_request_number: Annotated[int, "pull request number"],
    org_name: Annotated[str | None, "github organization name"] = None,
) -> str:
    """Use this tool for github. Get detailed file changes from a pull request including code changes."""
    try:
        repo = github_client.get_repo(repo_name, org_name)
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
                "patch": file.patch[:500] + "..."
                if file.patch and len(file.patch) > 500
                else file.patch,  # 실제 코드 변경 내용
                "raw_url": file.raw_url,
                "blob_url": file.blob_url,
            }
            result.append(file_info)

        return f"PR #{pull_request_number}의 파일 변경 정보: {result}"

    except Exception as e:
        return f"파일 변경 정보 조회 실패: {str(e)}"
