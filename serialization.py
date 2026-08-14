import csv
from dataclasses import dataclass, fields, asdict

def dataclasses_to_csv(items: list, path: str, filename: str) -> None:
    """
    Writes the dataclasses items in a CSV at the path provided.
    If the path folder does not exist, it is created.
    Args:
        items (list): Dataclasses to write in the CSV
        path (str): Path to the CSV
        filename (str): Filename of the CSV
    """
    path.mkdir(parents=True, exist_ok=True)

    fieldnames = [f.name for f in fields(items[0])]
    with open(path / filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(asdict(item))