from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    embeddings_model_name: str 
    embeddings_file_name: str
    model_name: str
    model_file_name: str
    faiss_index_path: str 
    ngrok_auth_token : str
    ngrok_edge: str
    use_ngrok: bool
    application_port: int
    database_url: str
    model_config = SettingsConfigDict(env_file=".env")