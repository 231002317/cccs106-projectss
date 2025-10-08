from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Literal

import flet as ft


# ------------------------------
# Data model and persistence
# ------------------------------

DATA_PATH = Path("data/todos.json")


@dataclass
class TodoItem:
    id: str
    title: str
    completed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "TodoItem":
        return TodoItem(
            id=str(data.get("id") or uuid.uuid4()),
            title=str(data.get("title", "")),
            completed=bool(data.get("completed", False)),
        )


def load_todos(filepath: Path = DATA_PATH) -> List[TodoItem]:
    if not filepath.exists():
        return []
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    items = data if isinstance(data, list) else data.get("todos", [])
    return [TodoItem.from_dict(it) for it in items]


def save_todos(items: List[TodoItem], filepath: Path = DATA_PATH) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    payload = [it.to_dict() for it in items]
    filepath.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


# ------------------------------
# UI application
# ------------------------------

FilterType = Literal["all", "active", "completed"]


def main(page: ft.Page) -> None:
    # Window and theme
    page.title = "Todo List"
    page.window_width = 400
    page.window_height = 640
    page.window_center()
    page.bgcolor = ft.Colors.BLUE_50
    page.theme_mode = ft.ThemeMode.LIGHT

    # State
    todos: List[TodoItem] = load_todos()
    current_filter: FilterType = "all"

    # Controls
    new_task_input = ft.TextField(
        hint_text="What needs to be done?",
        autofocus=True,
        expand=True,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
    )

    add_button = ft.IconButton(
        icon=ft.Icons.ADD_CIRCLE,
        icon_color=ft.Colors.GREEN,
        tooltip="Add task",
    )

    status_text = ft.Text(size=12, color=ft.Colors.BLUE_GREY)
    clear_completed_btn = ft.TextButton("Clear completed")

    list_view = ft.ListView(expand=True, spacing=8, auto_scroll=False)

    # Helpers
    def apply_filter(items: List[TodoItem]) -> List[TodoItem]:
        if current_filter == "active":
            return [t for t in items if not t.completed]
        if current_filter == "completed":
            return [t for t in items if t.completed]
        return items

    def refresh_list() -> None:
        list_view.controls.clear()
        for item in apply_filter(todos):
            list_view.controls.append(build_item_row(item))
        active_count = len([t for t in todos if not t.completed])
        status_text.value = f"{active_count} item{'s' if active_count != 1 else ''} left"
        page.update()

    def persist_and_refresh() -> None:
        save_todos(todos)
        refresh_list()

    # Item row builders
    def build_item_row(item: TodoItem) -> ft.Container:
        checkbox = ft.Checkbox(value=item.completed)
        title_text = ft.Text(
            value=item.title,
            size=14,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.BLACK87 if not item.completed else ft.Colors.BLUE_GREY,
            italic=item.completed,
            expand=True,
        )

        edit_field = ft.TextField(value=item.title, expand=True, dense=True)

        edit_mode = ft.Ref[ft.Container]()

        def toggle_complete(e) -> None:  # noqa: ANN001
            item.completed = bool(checkbox.value)
            persist_and_refresh()

        checkbox.on_change = toggle_complete

        def enter_edit_mode(e) -> None:  # noqa: ANN001
            container = edit_mode.current
            if container:
                container.content = build_edit_row()
                page.update()

        def save_edit(e) -> None:  # noqa: ANN001
            new_title = (edit_field.value or "").strip()
            if new_title:
                item.title = new_title
                persist_and_refresh()
            else:
                # empty title -> delete item
                delete_item()

        def cancel_edit(e) -> None:  # noqa: ANN001
            refresh_list()

        def confirm_delete(e) -> None:  # noqa: ANN001
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirm Deletion"),
                content=ft.Text(f"Delete '{item.title}'? This action cannot be undone."),
                actions=[
                    ft.TextButton("Cancel", on_click=lambda _: close_dialog(dialog)),
                    ft.TextButton("Delete", on_click=lambda _: (close_dialog(dialog), delete_item())),
                ],
            )
            open_dialog(dialog)

        def delete_item() -> None:
            nonlocal todos
            todos[:] = [t for t in todos if t.id != item.id]
            persist_and_refresh()

        def build_display_row() -> ft.Row:
            return ft.Row(
                controls=[
                    checkbox,
                    title_text,
                    ft.IconButton(icon=ft.Icons.EDIT, tooltip="Edit", on_click=enter_edit_mode),
                    ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete", icon_color=ft.Colors.RED, on_click=confirm_delete),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

        def build_edit_row() -> ft.Row:
            return ft.Row(
                controls=[
                    ft.Icon(ft.Icons.DRIVE_FILE_RENAME_OUTLINE, color=ft.Colors.BLUE_GREY),
                    edit_field,
                    ft.IconButton(icon=ft.Icons.CHECK, tooltip="Save", icon_color=ft.Colors.GREEN, on_click=save_edit),
                    ft.IconButton(icon=ft.Icons.CLOSE, tooltip="Cancel", on_click=cancel_edit),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

        container = ft.Container(
            ref=edit_mode,
            content=build_display_row(),
            bgcolor=ft.Colors.WHITE,
            padding=8,
            border_radius=8,
        )
        return container

    # Dialog helpers
    def open_dialog(dlg: ft.AlertDialog) -> None:
        page.dialog = dlg
        dlg.open = True
        page.update()

    def close_dialog(dlg: ft.AlertDialog) -> None:
        dlg.open = False
        page.update()

    # Add task logic
    def add_task(_: ft.ControlEvent | None = None) -> None:
        title = (new_task_input.value or "").strip()
        if not title:
            return
        todos.append(TodoItem(id=str(uuid.uuid4()), title=title, completed=False))
        new_task_input.value = ""
        persist_and_refresh()

    add_button.on_click = add_task
    new_task_input.on_submit = add_task

    # Filters
    def set_filter(filter_value: FilterType) -> None:
        nonlocal current_filter
        current_filter = filter_value
        persist_and_refresh()

    all_chip = ft.FilterChip(label=ft.Text("All"), selected=True, on_select=lambda e: set_filter("all"))
    active_chip = ft.FilterChip(label=ft.Text("Active"), on_select=lambda e: set_filter("active"))
    completed_chip = ft.FilterChip(label=ft.Text("Completed"), on_select=lambda e: set_filter("completed"))

    def update_chips() -> None:
        all_chip.selected = current_filter == "all"
        active_chip.selected = current_filter == "active"
        completed_chip.selected = current_filter == "completed"

    def on_chip_select(_: ft.ControlEvent) -> None:
        update_chips()
        refresh_list()

    all_chip.on_select = on_chip_select
    active_chip.on_select = on_chip_select
    completed_chip.on_select = on_chip_select

    # Clear completed
    def clear_completed(_: ft.ControlEvent | None = None) -> None:
        nonlocal todos
        todos[:] = [t for t in todos if not t.completed]
        persist_and_refresh()

    clear_completed_btn.on_click = clear_completed

    # Layout
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Row([
                        ft.Text("My Todo List", size=20, weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.CHECKLIST_RTL, color=ft.Colors.GREEN),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(
                        content=ft.Row([new_task_input, add_button]),
                        bgcolor=ft.Colors.WHITE,
                        padding=8,
                        border_radius=8,
                    ),
                    ft.Row([all_chip, active_chip, completed_chip], spacing=8),
                    ft.Container(content=list_view, expand=True),
                    ft.Row([status_text, clear_completed_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ],
                expand=True,
            ),
            padding=16,
            expand=True,
        )
    )

    # Initial render
    refresh_list()
    update_chips()


if __name__ == "__main__":
    ft.app(target=main)

