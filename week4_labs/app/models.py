from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any


@dataclass
class Contact:
    """Represents a single contact entry in the contact book.

    A Contact is uniquely identified by its id. For user-friendly access,
    name and email are also stored and validated by higher layers.
    """

    id: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Contact":
        return Contact(
            id=str(data.get("id", "")),
            first_name=str(data.get("first_name", "")),
            last_name=str(data.get("last_name", "")),
            phone=data.get("phone"),
            email=data.get("email"),
            address=data.get("address"),
            notes=data.get("notes"),
        )


@dataclass
class ContactBook:
    """In-memory container for contacts with basic operations."""

    contacts: Dict[str, Contact] = field(default_factory=dict)

    def add(self, contact: Contact) -> None:
        if contact.id in self.contacts:
            raise ValueError(f"Contact with id '{contact.id}' already exists")
        self.contacts[contact.id] = contact

    def update(self, contact_id: str, **updates: Any) -> Contact:
        if contact_id not in self.contacts:
            raise KeyError(f"Contact '{contact_id}' not found")
        contact = self.contacts[contact_id]
        for key, value in updates.items():
            if hasattr(contact, key) and value is not None:
                setattr(contact, key, value)
        return contact

    def remove(self, contact_id: str) -> None:
        if contact_id not in self.contacts:
            raise KeyError(f"Contact '{contact_id}' not found")
        del self.contacts[contact_id]

    def find_by_name(self, query: str) -> Dict[str, Contact]:
        q = query.strip().lower()
        result: Dict[str, Contact] = {}
        for cid, c in self.contacts.items():
            full_name = f"{c.first_name} {c.last_name}".strip().lower()
            if q in full_name:
                result[cid] = c
        return result

    def to_list(self) -> list[Contact]:
        return list(self.contacts.values())


