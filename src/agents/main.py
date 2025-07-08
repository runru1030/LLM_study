import asyncio
import sys

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent

from src.agents.mcp import get_mcp_client
from src.agents.model import ModelID, get_model
from src.tools.github import (
    get_pull_request_diff,
    get_pull_request_numbers,
)
from src.utils import pretty_print_messages

load_dotenv()

# 기본 시스템 프롬프트 정의
DEFAULT_SYSTEM_PROMPT = """You are an AI assistant that helps developers.

Primary Roles:
1. **Code Review Expert**: Analyze Pull Requests and provide detailed reviews from code quality, security, and performance perspectives.
2. **Development Guide**: Suggest code improvements and best practices.
3. **Problem Solver**: Identify potential issues in code and provide solutions.

Work Guidelines:
- Use get_pull_request_diff tool to get code diff of changed files.
- Do not use get_pull_request from github tools.
- Use tools minimally and efficiently.
- Provide practical and specific feedback from a developer's perspective.
- Consider various aspects including code style, architecture, security, and performance.
- Mention positive aspects while constructively suggesting improvements.

Language: Respond in English, maintaining technical terminology as is."""

# - Use get_pull_request_numbers tool to retrieve Pull Request numbers.

async def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "mcp"

    model = get_model(ModelID.OPENAI_GPT_41_MINI)

    match mode:
        case "mcp":
            client = get_mcp_client()
            tools = await client.get_tools()
            pass
        case "tool":
            tools = [
                get_pull_request_numbers,
                get_pull_request_diff,
            ]
            pass
        case _:
            raise ValueError(f"Invalid mode: {mode}")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", DEFAULT_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    agent = create_react_agent(model, tools, prompt=prompt)

    response = await agent.ainvoke(
        {
            "messages": "HITS-AI 조직의 ai-assistant 레포지토리에서 121번 PR의 변경 내용을 요약하고 개발자 관점에서 한국어로 자세히 리뷰해줘"
        },
    )
    pretty_print_messages(response)


asyncio.run(main())
