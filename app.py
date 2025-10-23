#!/usr/bin/env python3
"""
ReconAI - OSINT Intelligence Platform
Main application entry point
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from modules.domain_intel import DomainIntelligence
from modules.web_intel import WebIntelligence
from modules.network_intel import NetworkIntelligence
from modules.social_intel import SocialIntelligence
from modules.threat_intel import ThreatIntelligence
from modules.database import Database
from modules.llm_analyzer import LLMAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="ReconAI",
    description="OSINT Intelligence Platform for Defensive Security Testing",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize database
db = Database()

# Initialize modules
domain_intel = DomainIntelligence()
web_intel = WebIntelligence()
network_intel = NetworkIntelligence()
social_intel = SocialIntelligence()
threat_intel = ThreatIntelligence()
llm_analyzer = LLMAnalyzer()


class ReconRequest(BaseModel):
    """Request model for reconnaissance scan"""
    target: str
    scan_type: str = "full"  # full, quick, custom
    modules: List[str] = ["domain", "web", "network", "social", "threat"]


class ReconResponse(BaseModel):
    """Response model for reconnaissance results"""
    scan_id: str
    target: str
    status: str
    results: Dict[str, Any]
    analysis: Dict[str, Any]
    timestamp: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render main dashboard"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/scan", response_model=ReconResponse)
async def start_scan(recon_request: ReconRequest):
    """
    Start a new reconnaissance scan
    
    Args:
        recon_request: Scan configuration
        
    Returns:
        Scan results and analysis
    """
    try:
        scan_id = db.create_scan(recon_request.target, recon_request.scan_type)
        
        results = {}
        
        # Execute selected modules
        if "domain" in recon_request.modules:
            results["domain"] = await domain_intel.scan(recon_request.target)
            
        if "web" in recon_request.modules:
            results["web"] = await web_intel.scan(recon_request.target)
            
        if "network" in recon_request.modules:
            results["network"] = await network_intel.scan(recon_request.target)
            
        if "social" in recon_request.modules:
            results["social"] = await social_intel.scan(recon_request.target)
            
        if "threat" in recon_request.modules:
            results["threat"] = await threat_intel.scan(recon_request.target)
        
        # Perform LLM analysis
        analysis = await llm_analyzer.analyze(recon_request.target, results)
        
        # Save results to database
        db.save_results(scan_id, results, analysis)
        
        return ReconResponse(
            scan_id=scan_id,
            target=recon_request.target,
            status="completed",
            results=results,
            analysis=analysis,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/scans")
async def list_scans(limit: int = 10):
    """List recent scans"""
    scans = db.get_recent_scans(limit)
    return {"scans": scans}


@app.get("/api/scan/{scan_id}")
async def get_scan(scan_id: str):
    """Get scan results by ID"""
    scan = db.get_scan(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan


@app.get("/api/export/{scan_id}")
async def export_scan(scan_id: str, format: str = "json"):
    """Export scan results"""
    scan = db.get_scan(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    if format == "json":
        return JSONResponse(content=scan)
    elif format == "csv":
        # TODO: Implement CSV export
        raise HTTPException(status_code=501, detail="CSV export not yet implemented")
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")


@app.get("/api/stats")
async def get_stats():
    """Get platform statistics"""
    stats = db.get_statistics()
    return stats


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                      ReconAI v1.0                         ║
    ║         OSINT Intelligence Platform                       ║
    ║         Defensive Security Testing Suite                  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Initialize database
    db.initialize()
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

