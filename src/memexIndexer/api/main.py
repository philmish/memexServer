from typing import Literal
import uvicorn
import click
import os


@click.command(name="up")
@click.option(
    "--mode",
    default="debug",
    type=str,
    required=True
    )
@click.option(
    "--file",
    default="",
    type=str
    )
def up(mode, file) -> None:
    if mode == "debug" and file == "":
        os.environ["SERVER_MODE"] = "DEBUG"
        from memexIndexer.api.server import app
        uvicorn.run(app, host="127.0.0.1", port=9999)


if __name__ == "__main__":
    up()