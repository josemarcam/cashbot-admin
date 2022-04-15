from typer import Typer

from src.infra.cli import kafka, factories

def init_app(app: Typer):
    app.add_typer(kafka.app, name='kafka')
    app.add_typer(factories.app, name='factories')
