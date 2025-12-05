"""
Vercel-optimized API entry point for Claime AI
This file wraps the FastAPI app for Vercel serverless deployment
"""

from mangum import Mangum
from api import app

# Wrap FastAPI app with Mangum for AWS Lambda/Vercel compatibility
handler = Mangum(app, lifespan="off")
