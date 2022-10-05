import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

api_key = os.environ.get("OWM_API_KEY")
account_sid = "AC8b7e43c80171723d09f130606303abf6"
auth_token = os.environ.get("AUTH_TOKEN")

parameters = {
    "lat": 47.6,
    "lon": -122.33,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

res = requests.get("http://api.openweathermap.org/data/3.0/onecall", params=parameters)
res.raise_for_status()
data = res.json()

chance_of_rain = False
next_twelve_hours = data["hourly"][:12]
current_hr = 0
while not chance_of_rain and current_hr < len(next_twelve_hours):
    current_weather = next_twelve_hours[current_hr]["weather"]
    if current_weather[0]["id"] < 700:
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {"https": os.environ["https_proxy"]}
        client = Client(account_sid, auth_token, http_client=proxy_client)
        from_phone = os.environ.get("FROM_TWILIO_PHONE")
        to_phone = os.environ.get("TO_TWILIO_PHONE")
        message = client.messages.create(
            body="Rain in the forecast. Don't forget a rain jacket!",
            from_=from_phone,
            to=to_phone
        )
        chance_of_rain = True
    else:
        current_hr += 1

