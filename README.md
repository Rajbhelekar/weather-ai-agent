# 🌦️ Weather AI Agent

An AI-powered weather assistant built with Python and Ollama. It uses an LLM to understand natural-language questions and calls the Open-Meteo API to retrieve current weather information.

## ✨ Features

- Natural-language weather questions
- Current weather data using Open-Meteo
- Tool calling with Ollama (`qwen3:8b`)
- Temperature, feels-like temperature, humidity, wind speed, and precipitation
- Handles unknown cities and API errors
- Multi-turn conversations
- Automated tests using `unittest` and mocked API responses

## 🛠️ Tech Stack

- Python
- Ollama
- Qwen3 8B
- Requests
- Open-Meteo Geocoding API
- Open-Meteo Forecast API
- unittest

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Rajbhelekar/weather-ai-agent.git
cd weather-ai-agent
```

### 2. Install dependencies

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the packages:

```bash
pip install -r requirements.txt
```

### 3. Install and start Ollama

Install Ollama from https://ollama.com and download the model:

```bash
ollama pull qwen3:8b
```

### 4. Run the agent

```bash
python main.py
```

### 5. Run automated tests

```bash
python -m unittest test_weather.py -v
```

## 🌍 APIs

This project uses the Open-Meteo Geocoding API to find city coordinates and the Open-Meteo Forecast API to retrieve current weather data.

- https://open-meteo.com/

## 📁 Project Structure

```text
weather-ai-agent/
├── main.py
├── test_weather.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## 🧪 Testing

The tests use mocked API responses, so they do not require live API requests.

## 📌 Future Improvements

- More automated tests for edge cases
- Improved handling of API and model errors
- Cleaner response formatting
- Support for forecasts and additional weather queries

## 📄 License

This project is licensed under the MIT License.
