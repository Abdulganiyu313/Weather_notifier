import requests
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

api_key = "358af6bca2c3a9fe7128dda7b6200384"
lat = 6.524379
lon = 3.379206

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
    "units": "metric"  # Use "imperial" for Fahrenheit
}

response = requests.get(url, params=params) 
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
response.raise_for_status()  # Raise an error for bad responses    
data = response.json()

weather_main = data["weather"][0]["main"]
weather_description = data["weather"][0]["description"]
temperature = data["main"]["temp"]
humidity = data["main"]["humidity"]
wind_speed = data["wind"]["speed"]
city_name = data["name"]
country_name = data["sys"]["country"]

weather_msg = (
    f"🌍 Hello from {city_name}, {country_name}!\n\n"
    f"Here's your personalized weather update for today:\n"
    f"🌦️ Condition: {weather_main} — {weather_description.capitalize()}\n"
)

# Add explanation for weather conditions
condition_explanation = {
    "Clear": "☀️ It's sunny and clear—perfect weather to be outdoors!",
    "Clouds": "☁️ It's cloudy—skies are covered but it's still dry.",
    "Rain": "🌧️ It's raining—carry an umbrella and drive safely.",
    "Drizzle": "🌦️ Light rain or drizzle—watch your step on slippery surfaces.",
    "Thunderstorm": "⛈️ Thunderstorms expected—better to stay indoors.",
    "Snow": "❄️ Snowfall today—bundle up if you're going outside!",
    "Mist": "🌫️ Misty atmosphere—visibility might be low, be cautious."
}

weather_msg += condition_explanation.get(weather_main, "🔎 Weather condition explanation not available.\n")

weather_msg += (
    f"\n🌡️ Temperature: {temperature}°C — "
    f"{'Feels warm.' if temperature >= 25 else 'Feels cool.' if temperature < 18 else 'Comfortable.'}"
    f"\n💧 Humidity: {humidity}% — "
    f"{'Very humid, you might feel sticky.' if humidity > 70 else 'Fair humidity level.'}"
    f"\n💨 Wind Speed: {wind_speed} m/s — "
    f"{'Gusty winds, hold onto your hats!' if wind_speed > 5 else 'Light breeze.'}"
)

if "rain" in weather_main.lower() or "rain" in weather_description.lower():
    weather_msg += "\n\n☔ Heads up! Looks like rain — don’t forget your umbrella!"

weather_msg += "\n\nStay safe and enjoy the day, no matter the weather! 🌈"


my_email = "adeniyisulaiman27@gmail.com"
app_password = "qpuz cxqd jcxj bquy"
recipients = ["abdulganiyus03@gmail.com", "iwwaju@gmail.com", "wahajibola01@gmail.com"]

subject = "Today's Weather Update"
body = weather_msg

msg = MIMEMultipart()
msg["From"] = my_email
msg["To"] = ", ".join(recipients)
msg["Subject"] = subject

# Attach the body text using UTF-8
msg.attach(MIMEText(body, "plain", "utf-8"))

# Send the email
with SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=app_password)
    connection.sendmail(from_addr=my_email, to_addrs=recipients, msg=msg.as_string())

print("Email sent successfully!")