import requests
from twilio.rest import Client

OWM_Endpoint ="https://api.openweathermap.org/data/2.8/onecall"
api_key ="****"
account_sid = "****"
auth_token = "****"

weather_params = {
    "lat": 50.049683,
    "lon":  19.944544,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}
# 13.0826802
# 80.2707184
response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

a = 0
for a in range(0, 13):
    code_id = weather_data["hourly"][a]["weather"][0]["id"]
    if int(code_id) < 700:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="It's going to rain today remember to bring an umbrella",
            from_="+12526756663",
            to="****"
        )
        break
        print(message.status)
#+12526756663
