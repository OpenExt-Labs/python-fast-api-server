from fastapi import FastAPI
from loguru import logger

from src.application.profiling import ProfilingMiddleware
from src.config import settings
from src.infrastructure.application import create
from src.presentation import rest

# Initialize logger from loguru
logger.info("Application starting...")

# Create the application
app: FastAPI = create(
    debug=settings.debug,
    rest_routers=(
        rest.products.router,
        rest.orders.router,
        rest.auth.router,
        rest.users.router,
        rest.profiling.router
    ),
    startup_tasks=[],
    shutdown_tasks=[]
)

logger.info("Application started")

# Add middleware
app.add_middleware(ProfilingMiddleware)
