from fastapi import FastAPI

from src.infra.routes import health, user, auth, order


def get_routes() -> list:
    return [health, user, auth, order]


def init_app(app: FastAPI) -> None:
    app.include_router(health.router)
    app.include_router(user.router)
    app.include_router(auth.router)
    app.include_router(order.router)
