import os
from pydantic import BaseSettings

class SettingsBase(BaseSettings):
    """
    Represents a Base for API Settings.
    """
    db_host: str = "localhost"
    db_port: int = 27017
    rake_host: str = "127.0.0.1"
    rake_port: int = 3001

    @staticmethod
    def from_env_vars():
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        rake_host = os.getenv("RAKE_HOST")
        rake_port = os.getenv("RAKE_PORT")

        if db_host is None:
            raise Exception("Could not load env var for db_host")
        elif db_port is None:
            raise Exception("Could not load env var for db_port")
        elif db_port is None:
            raise Exception("Could not load env var for rake_host")
        elif rake_port is None:
            raise Exception("Could not load env var for rake_port")
        else:
            db_port = int(db_port)
            rake_port = int(rake_port)

        return SettingsBase(
                db_host=db_host,
                db_port=db_port,
                rake_host=rake_host,
                rake_port=rake_port
                )

default_settings = SettingsBase()
