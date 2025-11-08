"""
PersonaReflect Backend - FastAPI server for multi-agent system
"""
import os
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our agents
from persona_reflect.agents.orchestrator import PersonaReflectOrchestrator

# Data models
class DilemmaRequest(BaseModel):
    """Request model for journal entry"""
    user_id: str = "default_user"
    dilemma: str
    context: Dict[str, Any] = {}

class PersonaResponse(BaseModel):
    """Response from a single persona"""
    persona: str
    name: str
    icon: str
    response: str

class DilemmaResponse(BaseModel):
    """Complete response with all personas"""
    id: str
    timestamp: str
    dilemma: str
    responses: List[PersonaResponse]
    suggested_actions: List[str] = []

class ActionPlanRequest(BaseModel):
    """Request to create action plan"""
    entry_id: str
    responses: List[PersonaResponse]
    user_preferences: Dict[str, Any] = {}

class ActionPlan(BaseModel):
    """Action plan model"""
    id: str
    entry_id: str
    steps: List[str]
    created_at: str

# Initialize orchestrator
orchestrator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agents on startup"""
    global orchestrator
    print("🚀 Initializing PersonaReflect multi-agent system...")
    orchestrator = PersonaReflectOrchestrator()
    yield
    print("👋 Shutting down PersonaReflect...")

# Initialize FastAPI app
app = FastAPI(
    title="PersonaReflect API",
    description="Multi-agent system for self-reflection and personal growth",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "PersonaReflect API",
        "version": "1.0.0"
    }

@app.post("/api/reflect", response_model=DilemmaResponse)
async def get_reflections(request: DilemmaRequest):
    """
    Get diverse insights from all four AI personas
    """
    try:
        print(f"📝 Processing dilemma from user {request.user_id}")
        
        # Get responses from orchestrator
        result = await orchestrator.process_dilemma(
            user_id=request.user_id,
            dilemma=request.dilemma,
            context=request.context
        )
        
        # Format response
        response = DilemmaResponse(
            id=result["id"],
            timestamp=datetime.now().isoformat(),
            dilemma=request.dilemma,
            responses=result["responses"],
            suggested_actions=result.get("suggested_actions", [])
        )
        
        return response
        
    except Exception as e:
        print(f"❌ Error processing dilemma: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/action-plan", response_model=ActionPlan)
async def create_action_plan(request: ActionPlanRequest):
    """
    Synthesize persona insights into actionable steps
    """
    try:
        print(f"🎯 Creating action plan for entry {request.entry_id}")
        
        # Generate action plan using orchestrator
        plan = await orchestrator.create_action_plan(
            entry_id=request.entry_id,
            responses=request.responses,
            preferences=request.user_preferences
        )
        
        return ActionPlan(
            id=f"ap-{datetime.now().timestamp()}",
            entry_id=request.entry_id,
            steps=plan["steps"],
            created_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        print(f"❌ Error creating action plan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/personas")
async def get_personas():
    """
    Get information about available personas
    """
    return {
        "personas": [
            {
                "id": "cognitive-behavioral",
                "name": "Dr. Chen",
                "icon": "🧠",
                "title": "Cognitive-Behavioral Coach",
                "description": "Helps identify thought patterns and develop practical strategies"
            },
            {
                "id": "empathetic-friend",
                "name": "Maya",
                "icon": "💙",
                "title": "Empathetic Friend",
                "description": "Provides emotional support and validation"
            },
            {
                "id": "rational-analyst",
                "name": "Alex",
                "icon": "📊",
                "title": "Rational Analyst",
                "description": "Offers structured, data-driven approaches"
            },
            {
                "id": "mindfulness-mentor",
                "name": "Sage",
                "icon": "🧘",
                "title": "Mindfulness Mentor",
                "description": "Guides toward present-moment awareness"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "persona_reflect.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
