from langchain_mcp_adapters.client import MultiServerMCPClient

import os
from dotenv import load_dotenv

load_dotenv()


def get_mcp_client():
    mcp_config = {
        "github": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e",
                "GITHUB_PERSONAL_ACCESS_TOKEN",
                "ghcr.io/github/github-mcp-server",
            ],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_ACCESS_TOKEN")},
            "transport": "stdio",
        }
    }
    return MultiServerMCPClient(mcp_config)
