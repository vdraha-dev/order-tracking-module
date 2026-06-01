from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    debug: bool = True

    db_url: str = ""
    db_async_url: str = ""


config = Config()
