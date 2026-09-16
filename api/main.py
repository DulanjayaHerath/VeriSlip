"""
VeriSlip API Main Application.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.routes.verify import router as verify_router
from api.routes.forensics import router as forensics_router
from api.routes.webhook_whatsapp import router as whatsapp_router

app = FastAPI(
    title="VeriSlip Forensic API",
    description="AI-powered forensic tamper detection for bank transfer slips and payment receipts in P2P commerce.",
    version="1.0.0"
)

# Enable CORS for cross-origin web apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(verify_router)
app.include_router(forensics_router)
app.include_router(whatsapp_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "VeriSlip Forensic Engine",
        "version": "1.0.0",
        "supported_banks": ["COMBANK", "SAMPATH", "BOC", "HNB", "GENERIC_CEFTS"]
    }

# Mount static web directory
web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web"))
if os.path.exists(web_dir):
    app.mount("/static", StaticFiles(directory=web_dir), name="static")

    @app.get("/")
    def serve_cockpit():
        index_file = os.path.join(web_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "VeriSlip API is running. Web UI not found."}
