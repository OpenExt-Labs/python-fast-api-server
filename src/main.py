from fastapi import FastAPI
from loguru import logger

from src.application.profiling import ProfilingMiddleware
from src.config import settings
from src.infrastructure import application
from src.presentation import rest
from src.logging_config import logger

# Adjust the application
# -------------------------------
app: FastAPI = application.create(
    debug=settings.debug,
    rest_routers=(rest.products.router, rest.orders.router, rest.auth.router, rest.users.router, rest.profiling.router),
    startup_tasks=[],
    shutdown_tasks=[],
)

logger.error("Application started")

app.add_middleware(ProfilingMiddleware)
