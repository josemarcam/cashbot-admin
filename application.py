from fastapi import FastAPI
from fastapi_jwt_auth.auth_jwt import AuthJWT

from src.config import routes, containers, database, exceptions, auth
from fastapi_pagination import add_pagination

def create_app() -> FastAPI:
    container = containers.init_app()
    container.wire(modules=routes.get_routes())
    app = FastAPI()
    routes.init_app(app)
    exceptions.init_app(app)
    app.container = container
    add_pagination(app)
    return app


app = create_app()

@AuthJWT.load_config
def get_config():
    return auth.Settings()