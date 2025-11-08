# tools/calendar_tools.py
# All comments in English.

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone

from persona_reflect.services.gcal_demo import (
    gcal,
    suggest_slots,
    create_block as _gcreate,
)


def _now_utc() -> datetime:
    """Return timezone-aware UTC now."""
    return datetime.now(timezone.utc)


def _iso_utc(dt: datetime) -> str:
    """Return ISO8601 string in UTC with offset, no trailing Z."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def _normalize_incoming_iso(s: str) -> str:
    """Make incoming ISO acceptable to Python fromisoformat by converting Z to +00:00."""
    return s.replace("Z", "+00:00")


def list_events(days: int = 7) -> List[Dict[str, Any]]:
    """
    List upcoming events within the next `days` days from the primary calendar.
    Always uses timezone-aware UTC boundaries.
    """
    now = _now_utc()
    time_min = _iso_utc(now)
    time_max = _iso_utc(now + timedelta(days=int(days)))

    svc = gcal()
    items: List[Dict[str, Any]] = []
    page_token: Optional[str] = None

    while True:
        resp = (
            svc.events()
            .list(
                calendarId="primary",
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
                pageToken=page_token,
            )
            .execute()
        )

        for ev in resp.get("items", []):
            start = ev.get("start", {})
            end = ev.get("end", {})
            items.append(
                {
                    "id": ev.get("id", ""),
                    "summary": ev.get("summary", ""),
                    "start": start.get("dateTime") or start.get("date") or "",
                    "end": end.get("dateTime") or end.get("date") or "",
                    "htmlLink": ev.get("htmlLink", ""),
                    "status": ev.get("status", ""),
                }
            )

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return items


def find_free_time(
    days: int = 3,
    duration_minutes: int = 60,
    work_hours: Optional[List[int]] = None,
    topk: int = 3,
) -> List[Dict[str, Any]]:
    """
    Find available time slots using the helper.
    Args use only JSON-friendly types to support automatic function calling.
    """
    if work_hours is None:
        work_hours = [9, 18]
    start_h = max(0, int(work_hours[0]))
    end_h = min(24, int(work_hours[1]))
    if end_h <= start_h:
        end_h = min(start_h + 1, 24)

    slots = suggest_slots(
        days=int(days),
        duration=int(duration_minutes),
        work_hours=(start_h, end_h),  # helper expects a tuple; still fine internally
        topk=int(topk),
    )

    # Ensure plain JSON with strings only
    out: List[Dict[str, Any]] = []
    for s in slots:
        out.append(
            {
                "start": s.get("start", ""),
                "end": s.get("end", ""),
                "label": s.get("label", ""),
            }
        )
    return out


def create_block(
    title: str,
    start_iso: str,
    duration_minutes: int = 60,
    description: str = "",
) -> Dict[str, Any]:
    """
    Create an event block in the primary calendar.
    Accepts Z or offset; normalizes before passing down.
    """
    start_iso_norm = _normalize_incoming_iso(start_iso)
    created = _gcreate(
        title=title,
        start_iso=start_iso_norm,
        duration=int(duration_minutes),
        description=description,
    )
    return {
        "id": created.get("id", ""),
        "htmlLink": created.get("htmlLink", ""),
    }


CALENDAR_TOOL_FUNCS = [list_events, find_free_time, create_block]
