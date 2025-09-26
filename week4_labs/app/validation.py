from __future__ import annotations

import re
from typing import Optional


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[+\d][\d\-\s]{6,}$")


def validate_non_empty(value: str, field_name: str) -> str:
    v = (value or "").strip()
    if not v:
        raise ValueError(f"{field_name} cannot be empty")
    return v


def validate_email(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    v = value.strip()
    if v and not EMAIL_RE.match(v):
        raise ValueError("Invalid email format")
    return v or None


def validate_phone(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    v = value.strip()
    if v and not PHONE_RE.match(v):
        raise ValueError("Invalid phone format")
    return v or None


