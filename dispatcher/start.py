from api.handlers import register_exception_handlers
from api.middlewares import register_middlewares
from api.routing import register_routes
from fastapi import FastAPI



app = FastAPI(
    title="Taxi Dispatch API",
    description="Simulated taxi dispatch system with FastAPI + PostgreSQL",
    version="0.1.0",
    docs_url="/docs",  # Swagger
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",
)

# register middlewares
register_middlewares(app=app)

# register API routing
register_routes(app=app)

# register api exception handling
register_exception_handlers(app=app)
