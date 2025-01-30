from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    embeddings_model_name: str = "ChristianAzinn/snowflake-arctic-embed-xs-GGUF"
    embeddings_file_name: str = "snowflake-arctic-embed-xs--Q4_K_S.GGUF"
    model_name: str = "Qwen/Qwen2-0.5B-Instruct-GGUF"
    model_file_name: str = "*q8_0.gguf"
    faiss_index_path: str = "information_index"
    #ngrok_config = SettingsConfigDict(env_file=".env")