import asyncio
from langgraph.prebuilt import create_react_agent
from src.agents.model import ModelID, get_model
from dotenv import load_dotenv
from src.tools.github import (
    get_pull_requests,
    get_pull_request_changed_files,
)
from src.utils import pretty_print_messages
import os
import sys
from src.agents.mcp import get_mcp_client

load_dotenv()


async def main():
    mode = "mcp"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    model = get_model(ModelID.OPENAI_GPT_41_MINI)

    match mode:
        case "mcp":
            client = get_mcp_client()
            tools = await client.get_tools()
            pass
        case "tool":
            tools = [
                get_pull_requests,
                get_pull_request_changed_files,
            ]
            pass
        case _:
            raise ValueError(f"Invalid mode: {mode}")

    agent = create_react_agent(model, tools)
    response = await agent.ainvoke(
        {
            "messages": "HITS-AI 조직의 ai-assistant 레포지토리에서 open 상태의 pull request 리스트를 조회해줘 그리고 그 pull request의 파일 변경 파일 코드도 조회해줘"
        }
    )
    pretty_print_messages(response)


asyncio.run(main())
