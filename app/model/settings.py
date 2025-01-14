from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    google_client_id : str
    apple_client_id : str

    class Config:
        env_file = ".env"

settings = Settings()