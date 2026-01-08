import json
import boto3
import requests
import os
from datetime import datetime

s3 = boto3.client("s3")
BUCKET = "weather-data-els9cy"

# 5 major airports
AIRPORTS = {
    "CA": {"lat": 35.35474, "lon": -116.885329},
    "AS": {"lat": 34.9428028, "lon": -97.8180194},
    "AZ": {"lat": 34.3055992, "lon": -112.165001},
    "AA": {"lat": 38.704022, "lon": -101.473911},
    "WN": {"lat": 46.25, "lon": -117.249001}
}

# Read API key from Lambda environment variable
API_KEY = os.environ.get("OPENWEATHER_API_KEY")

def lambda_handler(event, context):
    if not API_KEY:
        raise ValueError("OPENWEATHER_API environment variable is not set.")

    for airport, coords in AIRPORTS.items():
        data_list = []

        lat = coords["lat"]
        lon = coords["lon"]

        # OpenWeatherMap API URL for current weather
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Convert to the same structure as before
            record = {
                "year": datetime.utcfromtimestamp(data["dt"]).year,
                "month": datetime.utcfromtimestamp(data["dt"]).month,
                "coord": {"lat": lat, "lon": lon},
                "main": {
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"]
                },
                "weather": [
                    {
                        "main": data["weather"][0]["main"],
                        "description": data["weather"][0]["description"]
                    }
                ],
                "wind": {
                    "speed": data["wind"]["speed"],
                    "deg": data["wind"]["deg"]
                },
                "dt": data["dt"]
            }

            data_list.append(record)
        else:
            print(f"Failed to fetch data for {airport}: {response.status_code} {response.text}")

        # Upload JSON to S3
        s3_key = f"weather/{airport}.json"
        s3.put_object(Bucket=BUCKET, Key=s3_key, Body=json.dumps(data_list))
        print(f"Saved {airport} weather data to {s3_key}")

    return {
        "statusCode": 200,
        "body": "Weather data fetched from API and saved to S3."
    }
