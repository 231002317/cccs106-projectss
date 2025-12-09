## CCCS 106 – Module 6 Learning Task: Weather Application Enhancement

This project is a Flet-based weather application built for **CCCS 106 - Application Development and Emerging Technologies**, Module 6: **System Integration and Network Programming**, based on the specification from the Weather Application Enhancement task [`mdeditor.net`](https://mdeditor.net/docs/a5df0c3659ed47ca873d6bff7be5f9f4).

### Base Application Features

- **City search**: Enter a city name (e.g., `Manila`) to fetch current weather.
- **Weather details**: Displays temperature, description, humidity, and wind speed.
- **Weather icons**: Uses OpenWeatherMap icon set for current conditions.
- **Async networking**: Uses `httpx.AsyncClient` with `page.run_task()` to avoid blocking the UI.
- **Error handling**: Gracefully handles invalid cities, network errors, and API issues.
- **Modern UI**: Built with Flet 0.28.3 and Material Design components.

### Enhanced Features Implemented

1. **Search History (Beginner Feature #1)**
   - Stores the last **up to 10** searched cities.
   - Shows them in a **dropdown** for quick reselection.
   - Persists history across sessions using a local JSON file: `search_history.json`.

2. **Temperature Unit Toggle (Beginner Feature #2)**
   - Adds a **switch** to toggle between **Celsius (°C)** and **Fahrenheit (°F)**.
   - Keeps a canonical temperature in Celsius and converts on the fly.
   - Does **not** refetch from the API when toggling, only converts the value.

### Project Structure

- `main.py` – Flet UI, OpenWeatherMap integration, async logic, and enhanced features.
- `config.py` – Loads the `OPENWEATHER_API_KEY` from environment variables using `python-dotenv`.
- `requirements.txt` – Python dependencies (generated from the virtual environment).
- `search_history.json` – Created at runtime to store search history (git-ignored).
- `env.example.txt` – Example environment configuration showing required variables.
- `.gitignore` – Ignores `venv/`, `.env`, `__pycache__/`, and other local files.

### Prerequisites

- Python 3.10+ (recommended)
- An **OpenWeatherMap API key** from `https://openweathermap.org/api`

### Setup Instructions (Local)

1. **Navigate to the project folder**:

```bash
cd cccs106-projects/mod6_labs
```

2. **(Optional if already created) Create and activate virtual environment**:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows PowerShell / CMD
# source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Create your `.env` file** next to `main.py`:

```bash
copy env.example.txt .env  # Windows
# cp env.example.txt .env  # macOS/Linux
```

Then edit `.env` and set your actual key:

```text
OPENWEATHER_API_KEY=your_real_openweathermap_api_key_here
```

5. **Run the application**:

```bash
python main.py
```

Flet will open a desktop window (or browser tab) showing the weather app.

### How to Use the App

1. Type a **city name** in the input field (e.g., `Manila`, `Tokyo`, `New York`).
2. Click **Search** or press **Enter**.
3. View the **current weather**, including:
   - Temperature (°C or °F depending on the toggle)
   - Weather description
   - Humidity %
   - Wind speed (m/s)
4. Use the **“Show in °F” switch** to toggle the temperature unit.
5. Use the **“Recent cities” dropdown** to quickly re-search previously queried cities.

### Screenshots (To Be Added by Student)

Include 3–5 screenshots in this folder, for example:

- `screenshot-1-home.png` – initial UI with no results.
- `screenshot-2-result.png` – city weather result in °C.
- `screenshot-3-toggle-fahrenheit.png` – same city with °F displayed.
- `screenshot-4-history-dropdown.png` – showing search history usage.

Then reference them in this README under this section.

### Notes on Async and Error Handling

- All network calls use `httpx.AsyncClient` with `await` for non-blocking IO.
- Long-running work is executed via `page.run_task()` as recommended in the task [`mdeditor.net`](https://mdeditor.net/docs/a5df0c3659ed47ca873d6bff7be5f9f4), avoiding `asyncio.create_task()` in event handlers.
- The app displays friendly messages for:
  - Invalid city names (404).
  - Network connectivity problems.
  - Unexpected API or server errors.

### Git and Submission Instructions (For You to Complete)

From `cccs106-projects`:

```bash
cd cccs106-projects
git init
git branch -M main
git add .
git commit -m "Add Module 6 weather application with enhancements"
```

Then create a GitHub repository named `cccs106-projects` and link it:

```bash
git remote add origin https://github.com/<your-username>/cccs106-projects.git
git push -u origin main
```

Your submission link for the LMS should be:

```text
https://github.com/<your-username>/cccs106-projects/tree/main/mod6_labs
```

### What You Still Need to Do

- Obtain your own **OpenWeatherMap API key** and put it in `.env`.
- Run the app and verify everything works on your machine.
- Capture and add **screenshots** to this folder and reference them in the README.
- Push to a **public** GitHub repo and submit the link as required by the task description.


