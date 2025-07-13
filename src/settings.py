import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')
load_dotenv(dotenv_path=Path(BASE_DIR).resolve().joinpath('env', ENVIRONMENT, '.env'))

DEBUG = os.getenv('DEBUG', 'False') == 'True'

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', False)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', False)
AWS_PROFILE_NAME = os.getenv('AWS_PROFILE_NAME', False)
AWS_REGION = os.getenv('AWS_REGION')
AWS_ASSUME_ROLE = os.getenv('AWS_ASSUME_ROLE', False)

IA_MODEL = "eu.anthropic.claude-sonnet-4-20250514-v1:0"
IA_TEMPERATURE = 0.3

BYPASS_TOOL_CONSENT = os.getenv('BYPASS_TOOL_CONSENT', 'False') == 'True'

MY_LATITUDE = float(os.getenv('MY_LATITUDE'))
MY_LONGITUDE = float(os.getenv('MY_LONGITUDE'))

LLM_READ_TIMEOUT = 300
LLM_CONNECT_TIMEOUT = 60
LLM_MAX_ATTEMPTS = 10
