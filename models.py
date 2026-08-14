from dataclasses import dataclass

@dataclass
class Character:
    name: str
    chapters: list[int]