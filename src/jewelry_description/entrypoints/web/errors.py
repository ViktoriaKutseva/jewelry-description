"""
Error handling middleware and custom exception handlers.
"""

from typing import Union
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from loguru import logger

from .schemas import ErrorResponse, ValidationErrorResponse


async def validation_exception_handler(request: Request, exc: Union[RequestValidationError, ValidationError]) -> JSONResponse:
    """
    Handle Pydantic validation errors.
    """
    logger.warning(
        "Validation error",
        url=str(request.url),
        method=request.method,
        errors=exc.errors() if hasattr(exc, 'errors') else str(exc)
    )

    if isinstance(exc, RequestValidationError):
        errors = exc.errors()
    else:
        errors = [{"loc": ["body"], "msg": str(exc), "type": "validation_error"}]

    # Transform errors to match ValidationErrorDetail structure
    transformed_errors = []
    for error in errors:
        # Convert ctx to string if it contains non-serializable objects
        ctx = error.get("ctx")
        if ctx is not None:
            # Convert any non-serializable objects in ctx to strings
            ctx = {k: str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v
                   for k, v in ctx.items()}

        transformed_error = {
            "loc": error.get("loc", []),
            "msg": error.get("msg", ""),
            "type": error.get("type", "validation_error"),
            "input": str(error.get("input", "")) if "input" in error else None,
            "ctx": ctx,
            "url": error.get("url")
        }
        transformed_errors.append(transformed_error)

    return JSONResponse(
        status_code=422,
        content=ValidationErrorResponse(
            detail=transformed_errors,
            type="validation_error",
            timestamp=None,  # Will be set by middleware if needed
        ).model_dump()
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions with proper logging.
    """
    logger.warning(
        "HTTP exception",
        url=str(request.url),
        method=request.method,
        status_code=exc.status_code,
        detail=exc.detail
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            type="http_error",
            timestamp=None,  # Will be set by middleware if needed
        ).model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions.
    """
    logger.error(
        "Unexpected error",
        url=str(request.url),
        method=request.method,
        error=str(exc),
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="Internal server error",
            type="internal_error",
            timestamp=None,  # Will be set by middleware if needed
        ).model_dump()
    )


def setup_error_handlers(app):
    """
    Register all error handlers with the FastAPI app.
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    logger.info("Error handlers registered")