from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import experiments, learning, service


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc) or "Service unavailable"},
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Nebibs Backend",
    description="Backend for Nebibs, connected to Supabase",
    version="0.1.0",
    lifespan=lifespan,
)
app.add_exception_handler(ValueError, value_error_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(learning.router)
app.include_router(experiments.router)
app.include_router(service.router)


@app.get("/")
async def root():
    return {"service": "nebibs-backend", "docs": "/docs"}
