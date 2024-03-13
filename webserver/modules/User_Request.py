from dataclasses import dataclass


@dataclass
class User_Request:
    location: dict
    days: int
    date_start: str
    date_end: str
