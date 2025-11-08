"""
Calendar and scheduling tools for action planning
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pydantic import BaseModel


class CalendarEvent(BaseModel):
    """Represents a calendar event"""
    title: str
    description: str
    start_time: datetime
    duration_minutes: int = 30
    priority: str = "medium"  # low, medium, high


class CalendarTool:
    """
    Simple calendar tool for scheduling action items.
    In production, integrate with Google Calendar API or similar.
    """
    
    def __init__(self):
        self.events: List[CalendarEvent] = []
    
    def suggest_time_slots(
        self,
        duration_minutes: int = 30,
        days_ahead: int = 7,
        preferred_hours: tuple = (9, 17)
    ) -> List[Dict[str, Any]]:
        """
        Suggest available time slots for scheduling an action.
        
        Args:
            duration_minutes: Duration of the activity
            days_ahead: How many days to look ahead
            preferred_hours: Tuple of (start_hour, end_hour) in 24h format
        
        Returns:
            List of suggested time slots
        """
        now = datetime.now()
        suggestions = []
        
        for day in range(1, days_ahead + 1):
            target_date = now + timedelta(days=day)
            
            # Morning slot (9 AM)
            if preferred_hours[0] <= 9 <= preferred_hours[1]:
                morning = target_date.replace(hour=9, minute=0, second=0, microsecond=0)
                suggestions.append({
                    "date": morning.strftime("%Y-%m-%d"),
                    "time": "09:00",
                    "datetime": morning.isoformat(),
                    "label": "Morning session"
                })
            
            # Lunch break (12 PM)
            if preferred_hours[0] <= 12 <= preferred_hours[1]:
                lunch = target_date.replace(hour=12, minute=0, second=0, microsecond=0)
                suggestions.append({
                    "date": lunch.strftime("%Y-%m-%d"),
                    "time": "12:00",
                    "datetime": lunch.isoformat(),
                    "label": "Midday break"
                })
            
            # Evening (6 PM)
            if preferred_hours[0] <= 18 <= preferred_hours[1]:
                evening = target_date.replace(hour=18, minute=0, second=0, microsecond=0)
                suggestions.append({
                    "date": evening.strftime("%Y-%m-%d"),
                    "time": "18:00",
                    "datetime": evening.isoformat(),
                    "label": "Evening wind-down"
                })
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def create_event(self, event: CalendarEvent) -> Dict[str, Any]:
        """
        Create a calendar event (mock implementation).
        In production, this would integrate with actual calendar APIs.
        """
        self.events.append(event)
        return {
            "success": True,
            "event_id": f"evt_{len(self.events)}",
            "message": f"Scheduled: {event.title} at {event.start_time.strftime('%Y-%m-%d %H:%M')}"
        }
    
    def get_upcoming_events(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get upcoming events"""
        now = datetime.now()
        cutoff = now + timedelta(days=days)
        
        upcoming = [
            {
                "title": evt.title,
                "start_time": evt.start_time.isoformat(),
                "duration": evt.duration_minutes,
                "priority": evt.priority
            }
            for evt in self.events
            if now <= evt.start_time <= cutoff
        ]
        
        return sorted(upcoming, key=lambda x: x["start_time"])
