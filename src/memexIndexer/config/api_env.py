from pydantic import BaseSettings

class SettingsBase(BaseSettings):
    """
    Represents a Base for API Settings.
    """
    db_host: str = "localhost"
    db_port: int = 27017
    rake_host: str = "127.0.0.1"
    rake_port: int = 3001

default_settings = SettingsBase()