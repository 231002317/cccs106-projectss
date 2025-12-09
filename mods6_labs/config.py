import os

from dotenv import load_dotenv


def load_config() -> str:
    """Load OpenWeatherMap API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENWEATHER_API_KEY is not set. "
            "Create a .env file based on .env.example and add your API key."
        )
    return api_key



