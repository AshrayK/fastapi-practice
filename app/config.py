from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_in : int

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8', 
        extra='ignore'  
    )

config = AppConfig()