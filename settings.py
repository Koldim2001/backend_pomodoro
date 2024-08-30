from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "ABC12345"
