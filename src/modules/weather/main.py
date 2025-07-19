import logging
from typing import Callable

from botocore.config import Config
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp import MCPTransport
from strands.tools.mcp.mcp_client import MCPClient
from strands.agent import AgentResult
from strands.models import BedrockModel
from strands_tools import calculator, file_write, current_time, think, python_repl

from core.aws import get_aws_session
from modules.weather.tools import Tools
from settings import (
    IA_MODEL, IA_TEMPERATURE, LLM_READ_TIMEOUT, LLM_CONNECT_TIMEOUT,
    LLM_MAX_ATTEMPTS, MY_LATITUDE, MY_LONGITUDE, )

logger = logging.getLogger(__name__)


def get_bedrock_model(
        read_timeout: int = LLM_READ_TIMEOUT,
        connect_timeout: int = LLM_CONNECT_TIMEOUT,
        max_attempts: int = LLM_MAX_ATTEMPTS) -> BedrockModel:
    config = Config(
        read_timeout=read_timeout,
        connect_timeout=connect_timeout,
        retries={'max_attempts': max_attempts}
    )
    session = get_aws_session()

    return BedrockModel(
        model_id=IA_MODEL,
        temperature=IA_TEMPERATURE,
        boto_session=session,
        boto_client_config=config,
    )

def get_agent(
        system_prompt: str,
        read_timeout: int = LLM_READ_TIMEOUT,
        connect_timeout: int = LLM_CONNECT_TIMEOUT,
        max_attempts: int = LLM_MAX_ATTEMPTS) -> Agent:
    base_tools = [calculator, think, python_repl, file_write, current_time]
    custom_tools = Tools(latitude=MY_LATITUDE, longitude=MY_LONGITUDE).get_tools()
    all_tools = base_tools + custom_tools

    bedrock_model = get_bedrock_model(
        read_timeout=read_timeout,
        connect_timeout=connect_timeout,
        max_attempts=max_attempts
    )
    return Agent(
        model=bedrock_model,
        tools=all_tools,
        system_prompt=system_prompt
    )

def ai_mcp(
        system_prompt: str,
        user_prompt: str,
        read_timeout: int = 300,
        connect_timeout: int = 60,
        max_attempts: int = 5) -> AgentResult:

    def create_streamable_http_transport():
        return streamablehttp_client("http://localhost:8888/mcp/")

    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

    with streamable_http_mcp_client:
        base_tools = [calculator, think, python_repl, file_write, current_time]
        mcp_tools = streamable_http_mcp_client.list_tools_sync()
        logger.info(f"Available MCP tools: {[tool.tool_name for tool in mcp_tools]}")
        all_tools = base_tools + mcp_tools

        bedrock_model = get_bedrock_model(
            read_timeout=read_timeout,
            connect_timeout=connect_timeout,
            max_attempts=max_attempts
        )

        agent = Agent(
            model=bedrock_model,
            tools=all_tools,
            system_prompt=system_prompt
        )
        return agent(user_prompt)

def ai(
        system_prompt: str,
        user_prompt: str,
        read_timeout: int = 300,
        connect_timeout: int = 60,
        max_attempts: int = 5) -> AgentResult:
    agent = get_agent(
        system_prompt=system_prompt,
        read_timeout=read_timeout,
        connect_timeout=connect_timeout,
        max_attempts=max_attempts)

    return agent(user_prompt)
