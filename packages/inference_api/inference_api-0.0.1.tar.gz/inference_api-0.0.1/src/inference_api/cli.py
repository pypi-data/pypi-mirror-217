import click
import uvicorn


@click.group()
def main_cli():
    pass


@main_cli.command()
@click.option("--reload", is_flag=True, help="Enable autoreload")
def start(reload):
    uvicorn.run("inference_api.main:app", host="0.0.0.0", port=8000, reload=reload)
