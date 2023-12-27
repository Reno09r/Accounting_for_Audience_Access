import attr
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

@attr.s
class Settings:
    bot_token = attr.ib(default=os.getenv("BOT_TOKEN"))
    model_config_env_file = attr.ib(default=os.getenv("MODEL_CONFIG_ENV_FILE", ".env"))
    model_config_env_file_encoding = attr.ib(default=os.getenv("MODEL_CONFIG_ENV_FILE_ENCODING", "utf-8"))

# Instantiate the Settings class
config = Settings()