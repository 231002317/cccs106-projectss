import flet as ft
import mysql.connector
from db_connection import connect_db


def main(page: ft.Page) -> None:
    # Page configuration
    page.title = "Ibarrientos Task Tracker"
    page.window_center()
    page.window_frameless = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_height = 350
    page.window_width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT

    # UI controls
    title_text = ft.Text(
        value="Ibarrientos Task Tracker",
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        text_align=ft.TextAlign.CENTER,
    )

    username_field = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        helper_text="This is your unique identifier",
        width=300,
        autofocus=True,
        enabled=True,
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
    )

    password_field = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        helper_text="This is your secret key",
        width=300,
        enabled=True,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.PASSWORD,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
    )

    async def login_click(e):  # noqa: ANN001
        username = (username_field.value or "").strip()
        password = (password_field.value or "").strip()

        # Dialogs
        success_dialog = ft.AlertDialog(
            title=ft.Text("Login Successful"),
            content=ft.Column(
                [
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN), ft.Text(f"Welcome, {username}!")],
                           alignment=ft.MainAxisAlignment.CENTER)
                ]
            ),
            actions=[ft.TextButton("OK", on_click=lambda _: close_dialog())],
        )

        failure_dialog = ft.AlertDialog(
            title=ft.Text("Login Failed"),
            content=ft.Column(
                [
                    ft.Row([ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED), ft.Text("Invalid username or password")],
                           alignment=ft.MainAxisAlignment.CENTER)
                ]
            ),
            actions=[ft.TextButton("OK", on_click=lambda _: close_dialog())],
        )

        invalid_input_dialog = ft.AlertDialog(
            title=ft.Text("Input Error"),
            content=ft.Column(
                [
                    ft.Row([ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE), ft.Text("Please enter username and password")],
                           alignment=ft.MainAxisAlignment.CENTER)
                ]
            ),
            actions=[ft.TextButton("OK", on_click=lambda _: close_dialog())],
        )

        database_error_dialog = ft.AlertDialog(
            title=ft.Text("Database Error"),
            content=ft.Text("An error occurred while connecting to the database"),
            actions=[ft.TextButton("OK", on_click=lambda _: close_dialog())],
        )

        def open_dialog(dlg: ft.AlertDialog) -> None:
            page.dialog = dlg
            dlg.open = True
            page.update()

        def close_dialog() -> None:
            if page.dialog:
                page.dialog.open = False
                page.update()

        # Validate inputs
        if not username or not password:
            open_dialog(invalid_input_dialog)
            return

        # Database logic
        try:
            conn = connect_db()
            cursor = conn.cursor()
            # Parameterized query to prevent SQL injection
            cursor.execute(
                "SELECT id FROM users WHERE username = %s AND password = %s",
                (username, password),
            )
            row = cursor.fetchone()
            conn.close()

            if row:
                open_dialog(success_dialog)
            else:
                open_dialog(failure_dialog)
        except mysql.connector.Error:
            open_dialog(database_error_dialog)

    login_button = ft.ElevatedButton(
        text="Login",
        width=100,
        icon=ft.Icons.LOGIN,
        on_click=login_click,
    )

    # Layout
    page.add(
        ft.Column(
            [
                title_text,
                ft.Container(
                    content=ft.Column([username_field, password_field], spacing=20),
                ),
                ft.Container(
                    content=ft.Row([login_button], alignment=ft.MainAxisAlignment.END),
                    margin=ft.margin.only(0, 20, 40, 0),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)


