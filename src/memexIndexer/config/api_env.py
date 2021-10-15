from pydantic import BaseSettings

class SettingsBase(BaseSettings):
    """
    Represents a Base for API Settings.
    """
    db_host: str = "localhost"
    db_port: int = 27017

default_settings = SettingsBase()