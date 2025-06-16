from flask import Flask, request, render_template
import requests
from datetime import datetime
from geopy.geocoders import Nominatim
from cryptography.fernet import Fernet

app = Flask(__name__)

ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def get_city_coordinates(city_name):
    geolocator = Nominatim(user_agent="satellite_alert_system")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError("City not found")

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

def is_iss_overhead(lat, long):
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])
    return (lat - 5 <= iss_lat <= lat + 5) and (long - 5 <= iss_long <= long + 5)

def is_night(lat, long):
    response = requests.get("https://api.sunrise-sunset.org/json", params={
        "lat": lat, "lng": long, "formatted": 0
    })
    data = response.json()
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    current_hour = datetime.utcnow().hour
    return current_hour <= sunrise_hour or current_hour >= sunset_hour

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        city = request.form.get("city")
        try:
            lat, long = get_city_coordinates(city)
            if not is_iss_overhead(lat, long) and is_night(lat, long):
                result = decrypt_data(encrypt_data("ISS is NOT overhead"))
            else:
                result = decrypt_data(encrypt_data("ISS is overhead"))
        except Exception as e:
            result = f"Error: {e}"
    return render_template("front_page.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
