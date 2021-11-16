import uvicorn
import os

os.environ["SERVER_MODE"] = "ENVVARS"
from memexIndexer.api.server import app
host = os.getenv("HOST")
port = os.getenv("PORT")
if host is None or port is None:
    raise Exception("Failed to load host and port from env vars.")
else:
    port = int(port)

uvicorn.run(app, host, port)
