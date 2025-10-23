#!/usr/bin/env python3
"""
ReconAI v2.0 - OSINT Intelligence Platform
Enhanced with Person Intelligence capabilities
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
from modules.person_intel import PersonIntelligence
from modules.database import Database
from modules.llm_analyzer import LLMAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="ReconAI v2.0",
    description="OSINT Intelligence Platform - Domain & Person Intelligence",
    version="2.0.0"
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
person_intel = PersonIntelligence()
llm_analyzer = LLMAnalyzer()


class ReconRequest(BaseModel):
    """Request model for reconnaissance scan"""
    target: str
    scan_type: str = "full"  # full, quick, custom
    target_type: str = "domain"  # domain or person
    modules: List[str] = ["domain", "web", "network", "social", "threat"]
    # Person-specific fields
    state: str = None
    dob: str = None


class ReconResponse(BaseModel):
    """Response model for reconnaissance results"""
    scan_id: str
    target: str
    target_type: str
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
    return {
        "status": "healthy",
        "version": "2.0.0",
        "features": ["domain_intel", "person_intel"],
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/scan", response_model=ReconResponse)
async def start_scan(recon_request: ReconRequest):
    """
    Start a new reconnaissance scan
    
    Supports both domain and person intelligence gathering
    """
    try:
        scan_id = db.create_scan(recon_request.target, recon_request.scan_type)
        
        results = {}
        
        # Person Intelligence Scan
        if recon_request.target_type == "person":
            print(f"[+] Starting person intelligence scan for: {recon_request.target}")
            
            # Run person intelligence module
            results["person"] = await person_intel.scan(
                recon_request.target,
                state=recon_request.state,
                dob=recon_request.dob
            )
            
            # Generate AI analysis for person
            analysis = await llm_analyzer.analyze(results, target_type="person")
            
        # Domain Intelligence Scan (original functionality)
        else:
            print(f"[+] Starting domain intelligence scan for: {recon_request.target}")
            
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
            
            # Generate AI analysis for domain
            analysis = await llm_analyzer.analyze(results, target_type="domain")
        
        # Update scan with results
        db.update_scan(scan_id, "completed", results, analysis)
        
        return ReconResponse(
            scan_id=scan_id,
            target=recon_request.target,
            target_type=recon_request.target_type,
            status="completed",
            results=results,
            analysis=analysis,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        print(f"[!] Scan error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/scan/{scan_id}")
async def get_scan(scan_id: str):
    """Get scan results by ID"""
    scan = db.get_scan(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan


@app.get("/api/scans")
async def list_scans(limit: int = 10):
    """List recent scans"""
    scans = db.get_recent_scans(limit)
    return {"scans": scans}


@app.get("/api/stats")
async def get_stats():
    """Get platform statistics"""
    stats = db.get_stats()
    return stats


if __name__ == "__main__":
    # Create required directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Banner
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                      ReconAI v2.0                         ║
    ║         OSINT Intelligence Platform                       ║
    ║         Domain & Person Intelligence Suite                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize database
    db.init_db()
    print("[+] Database initialized successfully")
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )

