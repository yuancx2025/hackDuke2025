# persona_reflect/agents/controllers/scheduler.py
from typing import Dict, Any, List
from persona_reflect.services.gcal_demo import suggest_slots as g_suggest, create_block as g_create


async def alex_suggest_with_slots(
    alex_text: str,
    days: int = 3,
    duration: int = 60,
    work_hours: tuple[int, int] = (9, 18),
    topk: int = 3,
) -> Dict[str, Any]:
    """
    Combine Alex's analytical suggestion with real Google Calendar slots.
    """
    slots = g_suggest(days=days, duration=duration, work_hours=work_hours, topk=topk)
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


async def book_slot(
    title: str, start_iso: str, duration: int = 60, description: str = ""
) -> Dict[str, Any]:
    """
    Create a real Google Calendar event.
    """
    created = g_create(
        title=title, start_iso=start_iso, duration=duration, description=description
    )
    return {"id": created["id"], "htmlLink": created["htmlLink"]}
