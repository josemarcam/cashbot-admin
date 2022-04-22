from fastapi import FastAPI
from fastapi_jwt_auth.auth_jwt import AuthJWT

from src.config import routes, containers, database, exceptions, auth
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    container = containers.init_app()
    container.wire(modules=routes.get_routes())
    app = FastAPI()
    origins = [
        "*"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    routes.init_app(app)
    exceptions.init_app(app)
    app.container = container
    add_pagination(app)
    return app


app = create_app()

@AuthJWT.load_config
def get_config():
    return auth.Settings()