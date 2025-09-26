from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Dict

from .models import Contact, ContactBook


class JsonStorage:
    """File-based JSON storage for contacts."""

    def __init__(self, filepath: Path) -> None:
        self.filepath = Path(filepath)

    def load(self) -> ContactBook:
        if not self.filepath.exists():
            return ContactBook()
        data = json.loads(self.filepath.read_text(encoding="utf-8"))
        contacts = {c["id"]: Contact.from_dict(c) for c in data.get("contacts", [])}
        return ContactBook(contacts=contacts)

    def save(self, book: ContactBook) -> None:
        payload = {"contacts": [c.to_dict() for c in book.to_list()]}
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.filepath.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def export_to_csv(contacts: Iterable[Contact], csv_path: Path) -> None:
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "address",
        "notes",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in contacts:
            writer.writerow(c.to_dict())


def import_from_csv(csv_path: Path) -> Dict[str, Contact]:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)
    imported: Dict[str, Contact] = {}
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contact = Contact.from_dict(row)
            imported[contact.id] = contact
    return imported


