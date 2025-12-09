import json
from pathlib import Path

import flet as ft
import httpx

from config import load_config


OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherApp:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.api_key = load_config()

        # temperature unit state
        self.current_unit = "metric"  # or "imperial"
        self.current_temp_c: float | None = None

        # search history state
        self.history_file = Path("search_history.json")
        self.search_history: list[str] = self.load_history()

        self.city_input = ft.TextField(
            label="City",
            hint_text="Enter city name (e.g., Manila)",
            autofocus=True,
            expand=True,
            on_submit=self.on_search_click,
        )
        self.search_button = ft.ElevatedButton(
            text="Search",
            icon=ft.icons.SEARCH,
            on_click=self.on_search_click,
        )

        self.unit_switch = ft.Switch(
            label="Show in °F",
            value=False,
            on_change=self.toggle_units,
        )

        self.history_dropdown = ft.Dropdown(
            label="Recent cities",
            hint_text="Select from history",
            options=[ft.dropdown.Option(city) for city in self.search_history],
            on_change=self.on_history_change,
            width=250,
        )

        self.status_text = ft.Text("", color=ft.colors.RED_400)

        self.weather_icon = ft.Image(height=80, width=80)
        self.temperature_text = ft.Text(size=32, weight=ft.FontWeight.BOLD)
        self.description_text = ft.Text(size=18)
        self.details_text = ft.Text(size=14)

        self.content_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [self.weather_icon, self.temperature_text],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        self.description_text,
                        self.details_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=20,
            ),
            elevation=4,
        )

        self.page.title = "Weather Application - CCCS 106"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.theme_mode = ft.ThemeMode.LIGHT

        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Weather Application",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Search for a city to see the current weather.",
                            size=14,
                            color=ft.colors.GREY,
                        ),
                        ft.Row(
                            controls=[self.city_input, self.search_button],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            controls=[self.unit_switch, self.history_dropdown],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Row(
                            controls=[self.status_text],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        self.content_card,
                    ],
                    spacing=15,
                    expand=False,
                ),
                padding=20,
                width=500,
            )
        )

    # ---------------- History handling ----------------
    def load_history(self) -> list[str]:
        if self.history_file.exists():
            try:
                with self.history_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return [str(c) for c in data][:10]
            except Exception:
                return []
        return []

    def save_history(self) -> None:
        try:
            with self.history_file.open("w", encoding="utf-8") as f:
                json.dump(self.search_history, f, ensure_ascii=False, indent=2)
        except Exception:
            # silently ignore file write issues for this simple app
            pass

    def add_to_history(self, city: str) -> None:
        city = city.strip()
        if not city:
            return
        if city in self.search_history:
            self.search_history.remove(city)
        self.search_history.insert(0, city)
        self.search_history = self.search_history[:10]
        self.save_history()

        self.history_dropdown.options = [
            ft.dropdown.Option(c) for c in self.search_history
        ]
        self.page.update()

    def on_history_change(self, e: ft.ControlEvent) -> None:
        selected_city = e.control.value
        if selected_city:
            self.city_input.value = selected_city
            self.page.update()
            self.on_search_click(e)

    async def fetch_weather(self, city: str) -> dict | None:
        """Fetch current weather data for the specified city."""
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(OPENWEATHER_BASE_URL, params=params)

        if response.status_code == 404:
            raise ValueError("City not found. Please check the spelling.")

        response.raise_for_status()
        return response.json()

    def on_search_click(self, e: ft.ControlEvent) -> None:
        """Start async weather fetch using page.run_task."""
        city = self.city_input.value.strip()

        if not city:
            self.show_error("Please enter a city name.")
            return

        # remember city in history
        self.add_to_history(city)

        self.status_text.value = "Fetching weather..."
        self.status_text.color = ft.colors.PRIMARY
        self.page.update()

        self.page.run_task(self.load_and_display_weather, city)

    async def load_and_display_weather(self, city: str) -> None:
        """Async task to fetch weather and update UI."""
        try:
            data = await self.fetch_weather(city)
        except ValueError as ve:
            self.show_error(str(ve))
            return
        except httpx.RequestError:
            self.show_error("Network error. Please check your internet connection.")
            return
        except httpx.HTTPStatusError:
            self.show_error("Unable to get weather data. Please try again later.")
            return
        except Exception:
            self.show_error("An unexpected error occurred.")
            return

        if not data:
            self.show_error("No data received from server.")
            return

        self.update_weather_display(data)

    def update_weather_display(self, data: dict) -> None:
        """Update the UI with weather data."""
        main = data.get("main", {})
        wind = data.get("wind", {})
        weather_list = data.get("weather", [])
        weather = weather_list[0] if weather_list else {}

        temp_c = main.get("temp")
        description = weather.get("description", "").title()
        humidity = main.get("humidity")
        wind_speed = wind.get("speed")
        icon_code = weather.get("icon")

        # store canonical temperature in Celsius for toggling
        if temp_c is not None:
            self.current_temp_c = float(temp_c)
        else:
            self.current_temp_c = None

        self.update_temperature_label()

        self.description_text.value = description or "No description available"
        self.details_text.value = (
            f"Humidity: {humidity}%   |   Wind: {wind_speed} m/s"
            if humidity is not None and wind_speed is not None
            else "Additional details unavailable"
        )

        if icon_code:
            self.weather_icon.src = (
                f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            )
        else:
            self.weather_icon.src = ""

        self.status_text.value = "Weather loaded successfully."
        self.status_text.color = ft.colors.GREEN
        self.page.update()

    def show_error(self, message: str) -> None:
        """Display error message in the status text."""
        self.status_text.value = message
        self.status_text.color = ft.colors.RED_400
        self.page.update()

    # ---------------- Unit toggle handling ----------------
    def update_temperature_label(self) -> None:
        """Update temperature text based on current unit and stored Celsius value."""
        if self.current_temp_c is None:
            self.temperature_text.value = "N/A"
            return

        if self.current_unit == "metric":
            self.temperature_text.value = f"{self.current_temp_c:.1f} °C"
        else:
            temp_f = (self.current_temp_c * 9 / 5) + 32
            self.temperature_text.value = f"{temp_f:.1f} °F"

    def toggle_units(self, e: ft.ControlEvent) -> None:
        """Toggle between Celsius and Fahrenheit without refetching data."""
        self.current_unit = "imperial" if e.control.value else "metric"
        self.update_temperature_label()
        self.page.update()


def main(page: ft.Page) -> None:
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)


