import logging

import click

from core.aws import setup_aws_conf
from modules.weather.main import ai
from modules.weather.prompts import PROMPT_TOOLS, SYSTEM_PROMPT
from settings import AWS_ASSUME_ROLE, AWS_REGION, AWS_PROFILE_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

logger = logging.getLogger(__name__)


@click.command()
def run():
    setup_aws_conf(
        assume_role=AWS_ASSUME_ROLE,
        region=AWS_REGION,
        profile_name=AWS_PROFILE_NAME,
        access_key_id=AWS_ACCESS_KEY_ID,
        secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    logger.info(f"Check agent weather.")

    _ = ai(
        system_prompt=SYSTEM_PROMPT,
        user_prompt="What will the weather be like tomorrow?")
