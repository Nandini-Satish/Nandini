# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import items, clock_in
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for different endpoints
app.include_router(items.router)
app.include_router(clock_in.router)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}
