from __future__ import annotations

import uuid
from pathlib import Path
from typing import List, Optional

from .models import Contact, ContactBook
from .storage import JsonStorage, export_to_csv, import_from_csv
from .validation import validate_non_empty, validate_email, validate_phone


class ContactService:
    """High-level operations for the Contact Book with validation and storage."""

    def __init__(self, data_path: Path) -> None:
        self.storage = JsonStorage(Path(data_path))
        self.book: ContactBook = self.storage.load()

    # CRUD
    def create_contact(
        self,
        first_name: str,
        last_name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Contact:
        first_name = validate_non_empty(first_name, "first_name")
        last_name = validate_non_empty(last_name, "last_name")
        phone = validate_phone(phone)
        email = validate_email(email)
        contact = Contact(
            id=str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            address=(address or None),
            notes=(notes or None),
        )
        self.book.add(contact)
        self.storage.save(self.book)
        return contact

    def list_contacts(self, sort_by: str = "last_name") -> List[Contact]:
        items = self.book.to_list()
        valid_keys = {"first_name", "last_name", "email", "phone"}
        key = sort_by if sort_by in valid_keys else "last_name"
        items.sort(key=lambda c: (getattr(c, key) or "").lower())
        return items

    def search(self, query: str) -> List[Contact]:
        results = self.book.find_by_name(query)
        return list(results.values())

    def update_contact(
        self,
        contact_id: str,
        *,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Contact:
        updates = {}
        if first_name is not None:
            updates["first_name"] = validate_non_empty(first_name, "first_name")
        if last_name is not None:
            updates["last_name"] = validate_non_empty(last_name, "last_name")
        if phone is not None:
            updates["phone"] = validate_phone(phone)
        if email is not None:
            updates["email"] = validate_email(email)
        if address is not None:
            updates["address"] = address or None
        if notes is not None:
            updates["notes"] = notes or None
        contact = self.book.update(contact_id, **updates)
        self.storage.save(self.book)
        return contact

    def delete_contact(self, contact_id: str) -> None:
        self.book.remove(contact_id)
        self.storage.save(self.book)

    # Import/Export
    def export_csv(self, csv_path: Path) -> None:
        export_to_csv(self.book.to_list(), Path(csv_path))

    def import_csv(self, csv_path: Path, overwrite: bool = False) -> int:
        imported = import_from_csv(Path(csv_path))
        count = 0
        for cid, contact in imported.items():
            if cid in self.book.contacts and not overwrite:
                continue
            if cid in self.book.contacts and overwrite:
                self.book.contacts[cid] = contact
            else:
                self.book.add(contact)
            count += 1
        self.storage.save(self.book)
        return count


