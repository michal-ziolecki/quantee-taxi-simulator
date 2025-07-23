from api.v1.routes import router as api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Taxi Dispatch API",
    description="Simulated taxi dispatch system with FastAPI + PostgreSQL",
    version="0.1.0",
    docs_url="/docs",  # Swagger
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",
)

# Optional: Enable CORS for local testing or frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(api_router, prefix="/api/v1")
