import requests
from datetime import datetime
APP_ID = "508ec464"
APP_KEY = "38c40825e4b0349b8a3c666db211e27d"
GENDER = "female"
WEIGHT_KG = 60
HEIGHT_CM = 170
AGE = 17

#endpoint
exercise_endpoint = " https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_address_endpoint = "https://api.sheety.co/55078ded0aeac2feb7eb12be08f421b9/workoutTracking/workouts"

headers = {
    "x-app-key": APP_KEY,
    "x-app-id": APP_ID
}
query = input("Tell me what exercises you did")
exercise_params = {
    "query": query,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=exercise_endpoint, json=exercise_params, headers=headers)
result = response.json()

# current date
today = datetime.now()
date_today = today.strftime("%d/%m/%Y")

# Time
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheety_inputs = {
        "workout" : {
            "date": date_today,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]

    }
    }

# Authentication
# sheet_response = requests.post(sheety_address_endpoint, json=sheety_inputs,
#   auth=(
#       "Dyuthi",
#       "atm29562",
#   )
#)
sheety_response = requests.post(url=sheety_address_endpoint, json=sheety_inputs)
print(sheety_response.text)
