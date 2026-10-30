from enums.ufcEventType import UfcEventType
import datetime


class UfcEvent:
    name: str
    type: UfcEventType
    number: int | None
    date: datetime.date
    city: str
    country: str
    arena: str
    preliminaryCardStartTime: datetime
    mainCardStartTime: datetime
