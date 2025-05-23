# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.routes import auth, documents, ingestions, users
# from app.models.database import engine, Base
# from app.core.config import settings
# import logging

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     description="Backend service for user and document management",
#     version="1.0.0"
# )

# # Configure CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.CORS_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Create tables on startup event
# @app.on_event("startup")
# def on_startup():
#     logging.info("Creating database tables (if not exist)...")
#     Base.metadata.create_all(bind=engine)
#     logging.info("Tables created")

# # Include routers with API prefix
# app.include_router(auth.router, prefix=settings.API_V1_STR)
# app.include_router(users.router, prefix=settings.API_V1_STR)
# app.include_router(documents.router, prefix=settings.API_V1_STR)
# app.include_router(ingestions.router, prefix=settings.API_V1_STR)

# @app.get("/")
# async def root():
#     return {"message": f"Welcome to {settings.PROJECT_NAME} API"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, documents, ingestions, users
from app.models.database import engine, Base
from app.core.config import settings
import logging
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logging.info("Creating database tables (if not exist)...")
    Base.metadata.create_all(bind=engine)
    logging.info("Tables created")
    yield
    # Optional: Shutdown logic here

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend service for user and document management",
    version="1.0.0",
    lifespan=lifespan  # modern lifecycle
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with API prefix
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(ingestions.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}
