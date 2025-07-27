from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from api.handlers import register_exception_handlers
from api.middlewares import register_middlewares
from api.routing import register_routes
from controllers.taxi_controller import taxi_controller
from fastapi import FastAPI
from loguru import logger
import typer
import uvicorn


console_app = typer.Typer()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup logic (optional)
    yield
    # Shutdown logic
    typer.echo(f"Taxi {taxi_controller.taxi_id} shutting down...")
    await taxi_controller.unregister_taxi()


api = FastAPI(
    title="Taxi Simulator API",
    description="Simulated taxi module",
    version="0.1.0",
    docs_url="/docs",  # Swagger
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# register middlewares
register_middlewares(app=api)

# register API routing
register_routes(app=api)

# register api exception handling
register_exception_handlers(app=api)


@console_app.command()
def start_taxi(
    network_id: str = typer.Option(
        "taxi-001", help="Taxi API address in the Docker network / service name"
    ),
    dispatcher_url: str = "http://dispatcher:8080",
) -> None:
    taxi_controller.network_id = network_id
    taxi_controller.dispatcher_url = dispatcher_url
    logger.info(
        f"Starting Taxi {taxi_controller.taxi_id} at "
        f"({taxi_controller.position_x}, {taxi_controller.position_x})"
        f" with network_id={network_id}, dispatcher_url={dispatcher_url}"
    )
    taxi_controller.register_taxi()
    uvicorn.run(api, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    typer.run(start_taxi)
