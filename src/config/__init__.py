from pydantic import BaseSettings

class CredentialsSettings(BaseSettings):
    SECRET_KEY: str

class Setting(CredentialsSettings):
    ...