import os


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost/dispatcher_db"
)
DISPATCHER_HOST = os.getenv("DISPATCHER_HOST", "0.0.0.0")
DISPATCHER_PORT = int(os.getenv("DISPATCHER_PORT", 8080))
