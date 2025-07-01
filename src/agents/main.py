import asyncio
from langgraph.prebuilt import create_react_agent
from src.agents.model import ModelID, get_model
from dotenv import load_dotenv
from src.tools.github import get_pull_requests, get_pull_request_changed_files
from src.utils import pretty_print_messages

load_dotenv()


async def main():
    model = get_model(ModelID.OPENAI_GPT_41_MINI)

    agent = create_react_agent(
        model, [get_pull_requests, get_pull_request_changed_files]
    )

    response = await agent.ainvoke(
        {
            "messages": "runru1030 계정의 LLM_study 레포지토리에서 pull request 리스트를 조회해줘 그리고 그 pr들의 파일 변경 세부 내용을 요약해줘"
        }
    )
    pretty_print_messages(response)


asyncio.run(main())
