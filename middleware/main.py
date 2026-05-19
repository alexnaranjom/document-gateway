from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, documents, categories
from app.config import APP_TITLE, APP_VERSION
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("middleware")

app = FastAPI(
    title=APP_TITLE,
    description=(
        "Modern Python middleware gateway for the Document Tracker. "
        "Provides authenticated access to the legacy document publishing system "
        "with request validation, audit logging, and OpenAPI documentation. "
        "Demonstrates the legacy system modernization pattern."
    ),
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS (required for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware (audit trail)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} duration={duration:.3f}s "
        f"client={request.client.host}"
    )
    return response


# Include routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "service": APP_TITLE,
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health",
    }