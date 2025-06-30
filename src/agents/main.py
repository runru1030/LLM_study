import asyncio
from langgraph.prebuilt import create_react_agent
from model import ModelID, get_model
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()


def pretty_print_messages(response):
    messages = response.get("messages") if isinstance(response, dict) else response
    if not isinstance(messages, list):
        messages = [messages]
    print("=" * 40)
    for msg in messages:
        # 객체 타입에 따라 역할 추출
        role = getattr(msg, "role", None) or getattr(msg, "type", None) or msg.__class__.__name__
        content = getattr(msg, "content", str(msg))
        print(f"[{role.upper()}]")
        print(content)
        print("-" * 40)
    print("=" * 40)


async def main():
    # OpenAI 모델 초기화
    model = get_model(ModelID.OLLAMA_LLAMA3_2)

    # API 키를 환경 변수에서 가져오기
    smithery_api_key = os.getenv("SMITHERY_API_KEY")
    if not smithery_api_key:
        raise ValueError("SMITHERY_API_KEY 환경 변수가 설정되지 않았습니다.")

    mcp_config = {
        "github": {
            "url": f"https://server.smithery.ai/@smithery-ai/github/mcp?api_key={smithery_api_key}&profile=still-limpet-6HJ8h2",
            "transport": "streamable_http",
        }
    }
    client = MultiServerMCPClient(mcp_config)
    tools = await client.get_tools()

    # MCP 도구로 React Agent 생성
    agent = create_react_agent(model, tools)

    # # 메시지를 통한 도구 호출
    response = await agent.ainvoke(
        {
            "messages": "runru1030 계정의 toss-fe-next2023 레포지토리에서 pull request 리스트를 조회해줘 그리고 그 pr들의 파일 변경사항을 조회해줘"
        }
    )
    pretty_print_messages(response)


# 비동기 실행
asyncio.run(main())
