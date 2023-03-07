import dotenv

env = dotenv.dotenv_values(".env")

# config parameters
TELEGRAM_BOT_TOKEN = env["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = env["OPENAI_API_KEY"]
OPENAI_ORG = env["OPENAI_ORG"]
