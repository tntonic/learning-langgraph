"""
FastAPI backend for Faropoint Tenant Research
Integrates with the LangGraph tenant research system
"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json
import asyncio
import uuid
from datetime import datetime
from sse_starlette.sse import EventSourceResponse

# Import our LangGraph tenant research system
from faropoint_tenant_demo import create_tenant_research_graph, TenantResearchState

app = FastAPI(title="Faropoint Tenant Research API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ResearchRequest(BaseModel):
    companyName: str
    location: str

class ResearchResponse(BaseModel):
    jobId: str
    status: str
    message: str

# In-memory job storage (use Redis in production)
research_jobs: Dict[str, Dict[str, Any]] = {}

# LangGraph instance
tenant_graph = create_tenant_research_graph()

async def run_tenant_research(job_id: str, company_name: str, location: str):
    """Run the tenant research workflow"""
    
    # Update job status
    research_jobs[job_id] = {
        "status": "running",
        "progress": [],
        "result": None,
        "error": None,
        "started_at": datetime.now().isoformat()
    }
    
    # Initialize state
    initial_state = {
        "company_name": company_name,
        "location": location,
        "industry": "",
        "website_url": None,
        "social_media_profiles": {},
        "online_reviews": [],
        "review_sentiment": 0.5,
        "business_registration": {},
        "years_in_business": None,
        "business_type": "",
        "is_verified": False,
        "estimated_revenue": None,
        "employee_count": None,
        "growth_indicators": [],
        "current_locations": [],
        "space_requirements": None,
        "lease_history": [],
        "litigation_history": [],
        "bankruptcy_flags": False,
        "negative_news": [],
        "risk_score": 0.5,
        "creditworthiness_indicators": [],
        "stability_score": 0.0,
        "growth_potential": 0.0,
        "overall_tenant_score": 0.0,
        "recommendation": "Not Recommended",
        "executive_summary": "",
        "key_concerns": [],
        "positive_factors": [],
        "messages": [],
        "data_sources": [],
        "confidence_level": 0.0
    }
    
    try:
        # Simulate step-by-step execution with progress updates
        steps = [
            ("identify", "Company Identification"),
            ("online", "Online Presence Analysis"),
            ("verify", "Business Verification"),
            ("financial", "Financial Indicators"),
            ("real_estate", "Real Estate History"),
            ("risk", "Risk Assessment"),
            ("score", "Tenant Scoring"),
            ("report", "Report Generation")
        ]
        
        for step_id, step_name in steps:
            # Update progress
            progress_update = {
                "stepId": step_id,
                "stepName": step_name,
                "status": "active",
                "timestamp": datetime.now().isoformat()
            }
            research_jobs[job_id]["progress"].append(progress_update)
            
            # Simulate processing time
            await asyncio.sleep(2)
            
            # Mark step as completed
            progress_update["status"] = "completed"
        
        # Run the actual graph (in production)
        # result = tenant_graph.invoke(initial_state)
        
        # For demo, create a mock result
        result = {
            "companyName": company_name,
            "location": location,
            "industry": "Technology",
            "recommendation": "Recommended",
            "overallScore": 75.5,
            "scores": {
                "stability": 0.82,
                "growth": 0.68,
                "risk": 0.25,
                "reputation": 0.85
            },
            "keyMetrics": {
                "yearsInBusiness": 5,
                "businessType": "LLC",
                "verified": True,
                "revenue": "$5-10M",
                "employees": "50-100",
                "currentLocations": 2
            },
            "strengths": [
                "Strong online reputation",
                "Verified business entity",
                "Consistent growth trajectory",
                "Multiple existing locations"
            ],
            "concerns": [
                "Limited financial history",
                "High employee turnover rate"
            ],
            "confidenceLevel": 0.85,
            "dataSources": 6
        }
        
        research_jobs[job_id]["status"] = "completed"
        research_jobs[job_id]["result"] = result
        research_jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        research_jobs[job_id]["status"] = "failed"
        research_jobs[job_id]["error"] = str(e)

@app.post("/api/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Start a new tenant research job"""
    job_id = str(uuid.uuid4())
    
    # Start background task
    background_tasks.add_task(
        run_tenant_research,
        job_id,
        request.companyName,
        request.location
    )
    
    return ResearchResponse(
        jobId=job_id,
        status="started",
        message=f"Research started for {request.companyName}"
    )

@app.get("/api/research/{job_id}")
async def get_research_status(job_id: str):
    """Get the status of a research job"""
    if job_id not in research_jobs:
        return {"error": "Job not found"}
    
    job = research_jobs[job_id]
    return {
        "jobId": job_id,
        "status": job["status"],
        "progress": job["progress"],
        "result": job["result"],
        "error": job["error"]
    }

@app.get("/api/research/{job_id}/progress")
async def research_progress_stream(job_id: str):
    """Server-sent events endpoint for real-time progress updates"""
    
    async def event_generator():
        while True:
            if job_id not in research_jobs:
                yield {
                    "event": "error",
                    "data": json.dumps({"message": "Job not found"})
                }
                break
            
            job = research_jobs[job_id]
            
            # Send progress updates
            if job["progress"]:
                latest_progress = job["progress"][-1]
                yield {
                    "event": "progress",
                    "data": json.dumps(latest_progress)
                }
            
            # Check if completed
            if job["status"] == "completed":
                yield {
                    "event": "complete",
                    "data": json.dumps(job["result"])
                }
                break
            
            # Check if failed
            if job["status"] == "failed":
                yield {
                    "event": "error",
                    "data": json.dumps({"message": job["error"]})
                }
                break
            
            await asyncio.sleep(1)
    
    return EventSourceResponse(event_generator())

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Faropoint Tenant Research API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)