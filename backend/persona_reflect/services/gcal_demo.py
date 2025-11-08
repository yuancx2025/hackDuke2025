# services/gcal_demo.py
# All comments in English.

import os
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Tuple
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# OAuth and Calendar config
SCOPES = [
    os.getenv("GOOGLE_CALENDAR_SCOPES", "https://www.googleapis.com/auth/calendar")
]
TOKEN_PATH = ".gcal_token.json"
CREDENTIALS_FILE = "credentials.json"
USER_TZ = os.getenv("GOOGLE_CALENDAR_TIMEZONE", "UTC")


# ---------- Time helpers (always timezone-aware) ----------


def _tz() -> ZoneInfo:
    """Return the ZoneInfo for USER_TZ, fallback to UTC on error."""
    try:
        return ZoneInfo(USER_TZ)
    except Exception:
        return ZoneInfo("UTC")


def _now_utc() -> datetime:
    """Timezone-aware current time in UTC."""
    return datetime.now(timezone.utc)


def _to_utc_iso(dt: datetime) -> str:
    """Return RFC3339 ISO for dt in UTC (with +00:00 offset)."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def _parse_iso_tolerant(s: str, default_tz: Optional[ZoneInfo] = None) -> datetime:
    """
    Parse ISO string supporting trailing 'Z'. If naive, attach default_tz (or UTC).
    Always return timezone-aware datetime.
    """
    s2 = s.replace("Z", "+00:00")
    dt = datetime.fromisoformat(s2)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=(default_tz or timezone.utc))
    return dt


def _localize_date_with_time(base: datetime, hour: int, minute: int = 0) -> datetime:
    """
    Given a base datetime (tz-aware), return a datetime on the same day with given hour/minute.
    """
    return base.replace(hour=hour, minute=minute, second=0, microsecond=0)


# ---------- Authorization & service ----------


def _authorize():
    """Authorize and build Google Calendar service client."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            # Use a local server flow for user consent
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


_svc = None


def gcal():
    """Return a singleton Calendar service client."""
    global _svc
    if not _svc:
        _svc = _authorize()
    return _svc


# ---------- Public helpers used by tool wrappers ----------


def suggest_slots(
    days: int = 3,
    duration: int = 60,
    work_hours: Tuple[int, int] = (9, 18),
    topk: int = 3,
) -> List[Dict]:
    """
    Suggest free time slots within the next `days` days.
    - All internal times are timezone-aware.
    - FreeBusy query uses UTC boundaries to avoid TZ ambiguity.
    Returns a list of {"start": iso, "end": iso, "label": str}.
    """
    tz = _tz()
    now_local = datetime.now(tz)

    # Normalize work hours
    start_h = max(0, int(work_hours[0]))
    end_h = min(24, int(work_hours[1]))
    if end_h <= start_h:
        end_h = min(start_h + 1, 24)

    # Search window: from "tomorrow at start_h" to "now + days at end_h"
    day1_local = now_local + timedelta(days=1)
    start_local = _localize_date_with_time(day1_local, start_h)
    end_local = _localize_date_with_time(now_local + timedelta(days=int(days)), end_h)

    # Convert window to UTC RFC3339
    time_min = _to_utc_iso(start_local)
    time_max = _to_utc_iso(end_local)

    fb = (
        gcal()
        .freebusy()
        .query(
            body={
                "timeMin": time_min,
                "timeMax": time_max,
                "items": [{"id": "primary"}],
                "timeZone": USER_TZ,
            }
        )
        .execute()
    )

    busy = fb["calendars"]["primary"].get("busy", [])

    # Normalize busy intervals to aware datetimes
    busy_intervals = []
    for b in busy:
        bs = _parse_iso_tolerant(b["start"], default_tz=timezone.utc)
        be = _parse_iso_tolerant(b["end"], default_tz=timezone.utc)
        busy_intervals.append((bs, be))

    # Cursor in UTC to compare apples-to-apples
    cursor = start_local.astimezone(timezone.utc)
    end_utc = end_local.astimezone(timezone.utc)
    gran = 30  # minutes between consecutive proposals
    out: List[Dict] = []

    def overlaps(
        a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime
    ) -> bool:
        return not (a_end <= b_start or a_start >= b_end)

    while cursor + timedelta(minutes=int(duration)) <= end_utc and len(out) < int(topk):
        block_end = cursor + timedelta(minutes=int(duration))
        conflict = False
        for bs, be in busy_intervals:
            # bs, be are aware (likely UTC from API), cursor/block_end are UTC
            if overlaps(cursor, block_end, bs, be):
                conflict = True
                # Jump cursor to the end of the busy block to skip overlap rapidly
                cursor = max(block_end, be)
                break

        if not conflict:
            # Render label in user's local timezone
            local_start = cursor.astimezone(tz)
            local_end = block_end.astimezone(tz)
            out.append(
                {
                    "start": cursor.isoformat(),
                    "end": block_end.isoformat(),
                    "label": local_start.strftime("%a %m/%d %H:%M")
                    + f" - {local_end.strftime('%H:%M')}",
                }
            )
            # Advance cursor by granularity beyond this suggestion
            cursor = block_end + timedelta(minutes=gran)

    return out


def create_block(
    title: str, start_iso: str, duration: int = 60, description: str = ""
) -> Dict:
    """
    Create a calendar event on the primary calendar.
    - Accepts ISO with 'Z' or explicit offset.
    - Stores with explicit timeZone=USER_TZ and localizes start in that zone.
    Returns {"id": ..., "htmlLink": ...}.
    """
    tz = _tz()
    # Parse start time, tolerate 'Z'; if naive, attach USER_TZ
    start_dt = _parse_iso_tolerant(start_iso, default_tz=tz).astimezone(tz)
    end_dt = start_dt + timedelta(minutes=int(duration))

    body = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": USER_TZ},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": USER_TZ},
    }
    created = (
        gcal()
        .events()
        .insert(calendarId="primary", body=body, sendUpdates="all")
        .execute()
    )
    return {"id": created.get("id"), "htmlLink": created.get("htmlLink")}
