from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    bot_admins: list[int]
    use_redis: bool

    db_host: str
    db_password: SecretStr
    db_user: str
    db_name: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

Config = Settings()
