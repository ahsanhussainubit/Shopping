from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    refresh_token_expire_days : int
    google_client_id : str
    apple_client_id : str
    redis_url : str
    redis_instances_count : int

    class Config:
        env_file = ".env"

settings = Settings()