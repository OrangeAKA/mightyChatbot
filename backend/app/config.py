from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "mighty-chatbot"
    environment: str = "development"
    log_level: str = "INFO"

    anthropic_api_key: str = ""

    # Added when auth layer lands (Day 3)
    # supabase_url: str = ""
    # supabase_anon_key: str = ""


settings = Settings()
