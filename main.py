import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

NAME = "Fulano"
GENDER = "Male"
WEIGHT_KG = "75"
HEIGHT_CM = "180"
AGE = "25"

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/b6608059c017dd384875855ebaec2927/workoutTracking/workouts"
exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID, # Id da aplicação
    "x-app-key": API_KEY, # Chave da aplicação
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
            "name": NAME
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, auth=(USER, PASSWORD))

    print(sheet_response.text) # Detalhes do exercício