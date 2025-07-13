from .check_weather import run as check_weather
from .forecast import run as forecast


def setup_commands(cli):
    cli.add_command(cmd=check_weather, name='check_weather')
    cli.add_command(cmd=forecast, name='forecast')
