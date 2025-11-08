"""
PersonaReflect - Multi-agent AI coaching system
"""

__version__ = "1.0.0"
__author__ = "HackDuke 2025 Team"

# Expose main components
from .agents.orchestrator import PersonaReflectOrchestrator
from .agents.cognitive_behavioral import CognitiveBehavioralAgent
from .agents.empathetic_friend import EmpatheticFriendAgent
from .agents.rational_analyst import RationalAnalystAgent
from .agents.mindfulness_mentor import MindfulnessMentorAgent

__all__ = [
    "PersonaReflectOrchestrator",
    "CognitiveBehavioralAgent",
    "EmpatheticFriendAgent", 
    "RationalAnalystAgent",
    "MindfulnessMentorAgent"
]