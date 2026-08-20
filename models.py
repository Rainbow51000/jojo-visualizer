from dataclasses import dataclass

@dataclass
class Character:
    name: str
    chapters: list[int]

@dataclass
class Relation:
    characters: set
    relation_type: str