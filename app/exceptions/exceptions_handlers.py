from asyncpg import ConnectionDoesNotExistError
from litestar import Request, Response
from sqlalchemy.exc import SQLAlchemyError

from app.core.custom_logger import logger
from app.exceptions.exceptions import NotFoundException


def not_found_exception_handler(_: Request, exc: NotFoundException) -> Response:
    return Response(status_code=404, content={"status_code": 404, "detail": str(exc)})


def database_connection_exception_handler(_: Request, exc: ConnectionDoesNotExistError) -> Response:
    logger.exception(exc)
    return Response(status_code=500, content={"status_code": 500, "detail": "Database connection error"})


def database_execute_exception_handler(_: Request, exc: SQLAlchemyError) -> Response:
    logger.exception(exc)
    return Response(status_code=500, content={"status_code": 500, "detail": "Database execute query error"})


exception_handlers = {
    NotFoundException: not_found_exception_handler,
    ConnectionDoesNotExistError: database_connection_exception_handler,
    SQLAlchemyError: database_execute_exception_handler
}
