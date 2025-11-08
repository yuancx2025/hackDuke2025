"""
PersonaReflect Backend - FastAPI server for multi-agent system
"""
import os
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager
from persona_reflect.services.gcal_demo import (
    gcal,
    suggest_slots as g_suggest,
    create_block as g_create,
)
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from persona_reflect.agents.rational_analyst import RationalAnalystAgent
from persona_reflect.agents.controllers.scheduler import (
    alex_suggest_with_slots,
    book_slot,
)
from persona_reflect.services.gcal_demo import gcal, TOKEN_PATH


# Load environment variables
load_dotenv()

# Import our agents
from persona_reflect.agents.orchestrator import PersonaReflectOrchestrator

alex_agent = RationalAnalystAgent()

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
    """Initialize agents on startup + auto Google Calendar auth"""
    global orchestrator
    print("🚀 Initializing PersonaReflect multi-agent system...")
    orchestrator = PersonaReflectOrchestrator()

    # --- Auto auth for Google Calendar (runs once at startup) ---
    try:
        token_abs = os.path.abspath(TOKEN_PATH)
        if not os.path.exists(token_abs):
            print(
                f"⚠️  No Google Calendar token found at {token_abs} — launching OAuth flow..."
            )
            _ = gcal()  # will open browser the first time; saves .gcal_token.json
            print("✅ Google Calendar authorized and token saved.")
        else:
            print(f"✅ Google Calendar token found at {token_abs}.")
    except Exception as e:
        # Do not crash the app; just log so you can retry from /api/calendar/auth
        print(f"❌ Calendar auth check failed: {e}")

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


@app.get("/api/calendar/auth")
async def calendar_auth():
    """
    Trigger OAuth once to authorize Google Calendar access.
    If a valid token already exists, this simply ensures the service is ready.
    """
    _ = gcal()  # lazily initializes and refreshes token; opens browser on first run
    return {"ok": True, "message": "Google Calendar authorized"}


@app.get("/api/calendar/suggest")
async def calendar_suggest(
    days: int = 3,
    duration: int = 60,
    start_hour: int = 9,
    end_hour: int = 18,
    topk: int = 3,
):
    """
    Suggest free time slots from the user's real Google Calendar.
    Returns up to `topk` slots of length `duration` minutes within [start_hour, end_hour].
    """
    slots = g_suggest(
        days=days, duration=duration, work_hours=(start_hour, end_hour), topk=topk
    )
    # Normalize to the shape your frontend/mock tool already expects
    normalized = [
        {
            "date": s["start"][:10],
            "time": s["start"][11:16],
            "datetime": s["start"],
            "label": s["label"],
            "end": s["end"],
        }
        for s in slots
    ]
    return {"slots": normalized}

@app.post("/api/calendar/book")
async def calendar_book(
    title: str = Query(..., description="Event title"),
    start_iso: str = Query(
        ..., description="RFC3339 datetime, e.g. 2025-11-09T09:00:00-05:00"
    ),
    duration: int = Query(60, description="Duration in minutes"),
    description: str = Query("", description="Optional description"),
):
    """
    Create a real Google Calendar event and return its calendar link.
    """
    created = g_create(
        title=title, start_iso=start_iso, duration=duration, description=description
    )
    return {"success": True, "id": created["id"], "htmlLink": created["htmlLink"]}


@app.post("/api/alex/schedule")
async def alex_schedule(
    dilemma: str = Query(..., description="What do you want to schedule?"),
    days: int = Query(3),
    duration: int = Query(60),
    start_hour: int = Query(9),
    end_hour: int = Query(18),
    topk: int = Query(3),
):
    """
    Use the existing orchestrator to get Alex's analysis text,
    then attach real Google Calendar free slots.
    """
    # 1) 用 orchestrator 生成四个角色的回复（这条路径你原来就稳定）
    result = await orchestrator.process_dilemma(
        user_id="default_user", dilemma=dilemma, context={}
    )

    # 2) 抽取 Alex 的文本（persona = 'rational-analyst' / name = 'Alex' 二者择一）
    alex_text = ""
    for r in result.get("responses", []):
        if r.get("persona") == "rational-analyst" or r.get("name") == "Alex":
            alex_text = r.get("response", "")
            break
    if not alex_text:
        alex_text = "Rational analysis: (fallback)\n- Define goal\n- Constraints\n- Options\n- Metrics\n- Timeline"

    # 3) 查询 Google Calendar 可用时间段
    slots = g_suggest(
        days=days, duration=duration, work_hours=(start_hour, end_hour), topk=topk
    )
    normalized = [
        {
            "label": s["label"],
            "start": s["start"],
            "end": s["end"],
            "date": s["start"][:10],
            "time": s["start"][11:16],
        }
        for s in slots
    ]
    return {"alex": alex_text, "slots": normalized}


@app.post("/api/alex/book")
async def alex_book(
    title: str = Query(..., description="Event title"),
    start_iso: str = Query(..., description="RFC3339 datetime"),
    duration: int = Query(60),
    description: str = Query("", description="Optional description"),
):
    """
    Create an event for the selected slot and return the Google Calendar link.
    """
    created = await book_slot(
        title=title, start_iso=start_iso, duration=duration, description=description
    )
    return {"success": True, **created}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "persona_reflect.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
