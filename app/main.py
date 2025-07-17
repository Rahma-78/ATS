# -*- coding: utf-8 -*-
"""
Main application file for the FastAPI ATS.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import routers
from app.core.config import settings

# --- Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# --- FastAPI App Initialization ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION,
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(routers.router, prefix=settings.API_V1_STR, tags=["Analysis"])

# --- Static Files ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")

from fastapi.responses import FileResponse

# --- Root Endpoint ---
@app.get("/")
async def root():
    return FileResponse("app/static/index.html")
