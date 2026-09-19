from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_env:str='development'
    cors_origins:list[str]=['http://localhost:5173']
    database_url:str='postgresql+asyncpg://videoforge:videoforge@postgres:5432/videoforge'
    redis_url:str='redis://redis:6379/0'
    object_store_endpoint:str='http://minio:9000'
    model_config=SettingsConfigDict(env_file='.env',extra='ignore')
settings=Settings()
