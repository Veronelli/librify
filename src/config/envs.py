from pydantic import BaseSettings


class MongoDBSetting(BaseSettings):
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str

class CredentialsSettings(BaseSettings):
    SECRET_KEY: str 

class Settings(CredentialsSettings, MongoDBSetting):
    ...

settings = Settings()