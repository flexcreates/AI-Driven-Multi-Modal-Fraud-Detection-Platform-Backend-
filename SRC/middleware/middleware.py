import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from SRC.logs.logger import get_logger

logger = get_logger("middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every incoming request with method, path, status code, and duration."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"

        logger.info(f"=> {request.method} {request.url.path} from {client_ip}")

        try:
            response = await call_next(request)
        except Exception as exc:
            duration = round((time.time() - start_time) * 1000, 2)
            logger.error(f"<= {request.method} {request.url.path} | 500 ERROR | {duration}ms | {exc}")
            raise

        duration = round((time.time() - start_time) * 1000, 2)
        logger.info(f"<= {request.method} {request.url.path} | {response.status_code} | {duration}ms")
        return response


# CORS configuration — Frontend team should update allowed_origins before deployment
CORS_CONFIG = {
    "allow_origins": [
        "http://localhost:3000",      # React dev server
        "http://localhost:5173",      # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
