from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    timestamp: datetime
    type: str
    message: str
    details: dict = field(default_factory=dict)


class EventGenerator:
    def __init__(self):
        self.events: list[Event] = []

    def add(self, event_type: str, message: str, **details) -> Event:
        event = Event(timestamp=datetime.utcnow(), type=event_type, message=message, details=details)
        self.events.append(event)
        return event

    def recent(self, limit: int = 20) -> list[dict]:
        return [
            {
                "timestamp": event.timestamp.isoformat(),
                "type": event.type,
                "message": event.message,
                "details": event.details,
            }
            for event in self.events[-limit:]
        ]
