import os
from fastapi.exceptions import HTTPException
import requests
from requests.sessions import session
from memexIndexer.api.routers.scraped_data.schemas import ScrapeRequest, ScrapedDataBase

try:
    mode = os.getenv("SERVER_MODE")
    if mode == "DEBUG":
        from memexIndexer.config.api_env import default_settings as settings
    # TODO Implement configs for hosting an env from files
    else:
        from memexIndexer.config.api_env import default_settings as settings

except Exception as e:
    # TODO Implement Exception for this case
    raise Exception(f"{e}\nrake client could not load environment.")


class RakeClient:
    """Client used for interaction with an rake api to scrape data."""
    def __init__(
        self,
        settings = settings
    ) ->None:
        self.settings = settings
        self.host = settings.rake_host
        self.port = settings.rake_port

    def make_request(self, req: ScrapeRequest):
        data = {
            "plugin": ScrapeRequest.plugin,
            "slug": ScrapeRequest.slug,
            "method": ScrapeRequest.method
            }
        resp = requests.post(f"{self.host}:{self.port}/scrape", json=data)
        if resp.status_code == 200:
            resp_data = resp.json()
            return ScrapedDataBase(**resp_data)
        else:
            raise HTTPException(
                status_code=resp.status_code,
                detail="rake server connection failed"
                )

