from __future__ import annotations

import argparse
from pathlib import Path

from app.service import ContactService


def build_parser():
    p = argparse.ArgumentParser(description="Contact Book Application")
    p.add_argument("command", choices=[
        "add", "list", "search", "update", "delete", "export", "import"
    ])
    p.add_argument("--data", dest="data", default=Path("data/contacts.json"), type=Path)

    # fields
    p.add_argument("--first", dest="first_name")
    p.add_argument("--last", dest="last_name")
    p.add_argument("--phone", dest="phone")
    p.add_argument("--email", dest="email")
    p.add_argument("--address", dest="address")
    p.add_argument("--notes", dest="notes")

    p.add_argument("--id", dest="contact_id")
    p.add_argument("--sort", dest="sort_by", default="last_name")
    p.add_argument("--q", dest="query")

    p.add_argument("--csv", dest="csv_path", type=Path)
    p.add_argument("--overwrite", action="store_true")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    svc = ContactService(args.data)

    if args.command == "add":
        contact = svc.create_contact(
            first_name=args.first_name or "",
            last_name=args.last_name or "",
            phone=args.phone,
            email=args.email,
            address=args.address,
            notes=args.notes,
        )
        print(contact.id)

    elif args.command == "list":
        for c in svc.list_contacts(sort_by=args.sort_by):
            print(f"{c.id} | {c.first_name} {c.last_name} | {c.phone or ''} | {c.email or ''}")

    elif args.command == "search":
        for c in svc.search(args.query or ""):
            print(f"{c.id} | {c.first_name} {c.last_name} | {c.phone or ''} | {c.email or ''}")

    elif args.command == "update":
        if not args.contact_id:
            raise SystemExit("--id is required for update")
        c = svc.update_contact(
            args.contact_id,
            first_name=args.first_name,
            last_name=args.last_name,
            phone=args.phone,
            email=args.email,
            address=args.address,
            notes=args.notes,
        )
        print(f"UPDATED {c.id}")

    elif args.command == "delete":
        if not args.contact_id:
            raise SystemExit("--id is required for delete")
        svc.delete_contact(args.contact_id)
        print("DELETED")

    elif args.command == "export":
        if not args.csv_path:
            raise SystemExit("--csv path is required for export")
        svc.export_csv(args.csv_path)
        print("EXPORTED")

    elif args.command == "import":
        if not args.csv_path:
            raise SystemExit("--csv path is required for import")
        count = svc.import_csv(args.csv_path, overwrite=args.overwrite)
        print(f"IMPORTED {count}")


if __name__ == "__main__":
    main()


