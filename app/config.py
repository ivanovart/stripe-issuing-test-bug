from pydantic import BaseSettings


class Settings(BaseSettings):
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    class Config:
        case_sensitive = True


settings = Settings()
