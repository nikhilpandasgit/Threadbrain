from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app
app = FastAPI(
    title="ThreadBrain API",
    version="1.0.0",
    description="Backend API for ThreadBrain application"
)

# Get CORS origins from environment variable
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "FastAPI backend is running 🚀", "status": "healthy"}

# Users endpoint
@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "Nik", "email": "nik@example.com"},
        {"id": 2, "name": "Kev", "email": "kev@example.com"}
    ]

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": os.getenv("ENVIRONMENT", "unknown")}

# Test endpoint for CORS
@app.get("/test")
def test_endpoint():
    return {"message": "CORS is working!", "origins": cors_origins}