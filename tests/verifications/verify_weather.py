import sys
import os

sys.path.append(os.getcwd())

try:
    from core.brain.weather_client import WeatherClient
    print("✅ Import successful")
except ImportError:
    print("❌ Import failed: WeatherClient not found")
    sys.exit(1)

client = WeatherClient()
weather = client.get_weather("Rowville")

print(f"Weather Report: {weather}")

if weather and isinstance(weather, str) and ("C" in weather or "F" in weather):
    print("✅ Weather fetch successful")
    sys.exit(0)
else:
    print("❌ Weather fetch failed or invalid format")
    sys.exit(1)
