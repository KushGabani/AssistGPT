import dotenv
from pathlib import Path

env = dotenv.dotenv_values(".env")

# config parameters
telegram_token = env["TELEGRAM_BOT_TOKEN"]
openai_api_key = env["OPENAI_API_KEY"]
openai_org = env["OPENAI_ORG"]
