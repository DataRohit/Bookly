import logging
import time

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            return JSONResponse(
                content={"message": "Internal Server Error", "error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        processing_time = time.time() - start_time
        message = (
            f"{request.client.host}:{request.client.port} - {request.method} "
            f"- {request.url.path} - {response.status_code} completed in {processing_time:.4f}s"
        )
        print(message)
        return response

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
        ],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["Content-Type", "Authorization"],
        allow_credentials=True,
    )
