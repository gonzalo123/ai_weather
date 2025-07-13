import logging

from commands import setup_commands
from core.cli import cli

setup_commands(cli)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level="INFO",
    datefmt="%d/%m/%Y %X",
)

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    cli()
