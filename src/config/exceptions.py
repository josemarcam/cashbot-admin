from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from src.shared.exceptions import (
    ValidationException,
    NotFoundException,
    ForbiddenException,
    BadRequestException,
    InternalServerErrorException,
    UnauthorizedException
)


def init_app(app: FastAPI):

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, error: AuthJWTException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "message": error.message
            }
        )
    
    @app.exception_handler(ValidationException)
    def validation_error(request: Request, error: ValidationException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "data": error.to_dict(),
                "message": error.message
            }
        )

    @app.exception_handler(NotFoundException)
    def not_found_error(request: Request, error: NotFoundException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "data": error.to_dict(),
                "message": error.message
            }
        )

    @app.exception_handler(ForbiddenException)
    def forbidden_error(request: Request, error: ForbiddenException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "data": error.to_dict(),
                "message": error.message
            }
        )

    @app.exception_handler(BadRequestException)
    def bad_request_error(request: Request, error: BadRequestException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "data": error.to_dict(),
                "message": error.message
            }
        )

    @app.exception_handler(InternalServerErrorException)
    def internal_server_error(request: Request, error: InternalServerErrorException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "data": error.to_dict(),
                "message": error.message
            }
        )

    @app.exception_handler(UnauthorizedException)
    def unauthorized_error(request: Request, error: UnauthorizedException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "response": error.status_code,
                "data": error.to_dict(),
                "message": error.message
            }
        )