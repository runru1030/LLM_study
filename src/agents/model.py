import os
import typing
from enum import StrEnum
from functools import cache
from typing import Any, Callable, Sequence, Union

from langchain_aws import ChatBedrockConverse
from langchain_core.language_models import (
    BaseChatModel,
    FakeListChatModel,
    LanguageModelInput,
)
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

__all__ = ("ModelID", "get_model")

load_dotenv()


class CustomFakeListChatModel(FakeListChatModel):
    def bind_tools(
        self,
        tools: Sequence[
            Union[typing.Dict[str, Any], type, Callable, BaseTool]  # noqa: UP006
        ],
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        return self


class ModelID(StrEnum):
    CLAUDE_HAIKU = "anthropic.claude-3-5-haiku-20241022-v1:0"
    OLLAMA_LLAMA3_2 = "llama3.2"
    OLLAMA_LLAMA3_2_1B = "llama3.2:1b"
    OPENAI_GPT_41_MINI = "gpt-4.1-mini"
    FAKE = "fake"


@cache
def get_model(model_id: ModelID, temperature: float = 0.5) -> BaseChatModel:
    match model_id:
        case ModelID.CLAUDE_HAIKU:
            return ChatBedrockConverse(
                model=model_id,  # noqa: ignore
                region_name="us-west-2",  # noqa: ignore
                # temperature=temperature,
                temperature=0,
                max_tokens=4096,
                # max_tokens=8191,
            )
        case ModelID.OLLAMA_LLAMA3_2:
            return ChatOllama(model="llama3.2", temperature=0.3)
        case ModelID.OLLAMA_LLAMA3_2_1B:
            return ChatOllama(model="llama3.2:1b", temperature=0.3)
        case ModelID.OPENAI_GPT_41_MINI:
            return ChatOpenAI(
                model_name=model_id,
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                temperature=temperature,
            )
        case ModelID.FAKE:
            return CustomFakeListChatModel(responses=["Fake response."])
        case _:
            raise NotImplementedError(f"Model {model_id} is not implemented.")
