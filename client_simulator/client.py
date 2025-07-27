import random
from uuid import UUID, uuid4

import httpx
import typer


app = typer.Typer()

GRID_MIN = 1
GRID_MAX = 100


def random_coord() -> int:
    return random.randint(GRID_MIN, GRID_MAX)


@app.command()
def request_ride(
    host: str = "http://localhost:8080",
    user_id: UUID = uuid4(),
    pickup_x: int | None = typer.Option(None, help="Pickup X coordinate (1-100)"),
    pickup_y: int | None = typer.Option(None, help="Pickup Y coordinate (1-100)"),
    dropoff_x: int | None = typer.Option(None, help="Dropoff X coordinate (1-100)"),
    dropoff_y: int | None = typer.Option(None, help="Dropoff Y coordinate (1-100)"),
) -> None:
    """Simulate a client sending a ride request to the dispatcher."""

    url = f"{host}/api/v1/trip/request"
    x1 = pickup_x or random_coord()
    y1 = pickup_y or random_coord()
    x2 = dropoff_x or random_coord()
    y2 = dropoff_y or random_coord()
    payload = {
        "user_id": str(user_id),
        "pickup_x": x1,
        "pickup_y": y1,
        "dropoff_x": x2,
        "dropoff_y": y2,
    }

    typer.echo(f"Sending client request to {url} ...")
    typer.echo(f"Payload: {payload}")

    try:
        response = httpx.post(url, json=payload)
        response.raise_for_status()
        typer.echo(f"Success: {response.json()}")
    except httpx.HTTPStatusError as e:
        typer.echo(f"Error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        typer.echo(f"Unexpected error: {e}")


if __name__ == "__main__":
    typer.run(request_ride)
