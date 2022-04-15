from typer import Typer

from src.config import cli, containers, database

def create_app() -> Typer:
    container = containers.init_app()
    app = Typer()
    app.container = container
    cli.init_app(app)
    return app

app = create_app()

if __name__ == '__main__':
    app()