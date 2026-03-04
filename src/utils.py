
import base64
import logging
from typing import Optional, Tuple

import requests

class GitHubAPI:
    """A wrapper for the GitHub API to manage repository actions."""

    def __init__(self, api_key: str, owner: str, repo: str):
        """Initializes the GitHubAPI client.

        Args:
            api_key: Your GitHub personal access token.
            owner: The owner of the repository.
            repo: The name of the repository.
        """
        self.api_key = api_key
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = {
            "Authorization": f"token {api_key}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_readme_content(self) -> Tuple[str, str]:
        """Fetches the content and SHA of the README.md file."""
        url = f"{self.base_url}/readme"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        return content, data["sha"]

    def get_default_branch(self) -> str:
        """Gets the default branch of the repository."""
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["default_branch"]

    def get_latest_commit_sha(self, branch: Optional[str] = None) -> str:
        """获取分支上最新提交的 SHA。

        Gets the SHA of the latest commit on a branch."""
        if branch is None:
            branch = self.get_default_branch()
        url = f"{self.base_url}/git/ref/heads/{branch}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["object"]["sha"]

    def create_branch(self, new_branch: str, base_branch: Optional[str] = None):
        """从一个基础分支创建一个新分支。

        Creates a new branch from a base branch."""
        if base_branch is None:
            base_branch = self.get_default_branch()
        base_sha = self.get_latest_commit_sha(base_branch)
        url = f"{self.base_url}/git/refs"
        payload = {
            "ref": f"refs/heads/{new_branch}",
            "sha": base_sha
        }
        response = requests.post(url, headers=self.headers, json=payload)
        # 如果分支已存在，将返回 422 错误。我们可以忽略它。
        # If the branch already exists, a 422 is returned. We can ignore it.
        if response.status_code != 422:
            response.raise_for_status()

    def create_or_update_file(self, file_path: str, commit_message: str, content: str, branch: str, sha: Optional[str] = None):
        """Creates or updates a file in the repository."""
        url = f"{self.base_url}/contents/{file_path}"
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        
        payload = {
            "message": commit_message,
            "content": encoded_content,
            "branch": branch
        }
        if sha:
            payload["sha"] = sha
            
        response = requests.put(url, headers=self.headers, json=payload)
        response.raise_for_status()

    def create_pull_request(self, title: str, body: str, head: str, base: str) -> str:
        """创建一个拉取请求。

        Creates a pull request."""
        url = f"{self.base_url}/pulls"
        payload = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()["html_url"]
