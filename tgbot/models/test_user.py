from dataclasses import dataclass


@dataclass
class TestUser:
    id: int
    name: str
    telegram_id: int
    status: int
