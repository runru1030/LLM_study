import asyncio
from langgraph.prebuilt import create_react_agent
from src.agents.model import ModelID, get_model
from dotenv import load_dotenv
from src.tools.github import (
    get_pull_requests,
    get_pull_request_changed_files,
)
from src.utils import pretty_print_messages

load_dotenv()


async def main():
    model = get_model(ModelID.OPENAI_GPT_41_MINI)

    tools = [
        get_pull_requests,
        get_pull_request_changed_files,
    ]

    agent = create_react_agent(model, tools)

    response = await agent.ainvoke(
        {
            "messages": "HITS-AI 조직의 argocd 레포지토리에서 open 상태의 pull request 리스트를 조회해줘 그리고 그 pull request의 파일 변경 파일 코드도 조회해줘"
        }
    )
    pretty_print_messages(response)


asyncio.run(main())
