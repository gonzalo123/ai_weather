import logging

from botocore.config import Config
from strands import Agent
from strands.agent import AgentResult
from strands.models import BedrockModel
from strands_tools import calculator, file_write, current_time, think, python_repl

from core.aws import get_aws_session
from modules.weather.tools import Tools
from settings import (
    IA_MODEL, IA_TEMPERATURE, LLM_READ_TIMEOUT, LLM_CONNECT_TIMEOUT,
    LLM_MAX_ATTEMPTS, MY_LATITUDE, MY_LONGITUDE, )

logger = logging.getLogger(__name__)


def get_agent(
        system_prompt: str,
        read_timeout: int = LLM_READ_TIMEOUT,
        connect_timeout: int = LLM_CONNECT_TIMEOUT,
        max_attempts: int = LLM_MAX_ATTEMPTS) -> Agent:
    config = Config(
        read_timeout=read_timeout,
        connect_timeout=connect_timeout,
        retries={'max_attempts': max_attempts}
    )
    session = get_aws_session()

    base_tools = [calculator, think, python_repl, file_write, current_time]
    custom_tools = Tools(latitude=MY_LATITUDE, longitude=MY_LONGITUDE).get_tools()
    all_tools = base_tools + custom_tools

    bedrock_model = BedrockModel(
        model_id=IA_MODEL,
        temperature=IA_TEMPERATURE,
        boto_session=session,
        boto_client_config=config,
    )
    return Agent(
        model=bedrock_model,
        tools=all_tools,
        system_prompt=system_prompt
    )


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
