#!/usr/bin/python3

# -------------------------
# Standard library imports
# -------------------------
import tkinter as tk
from tkinter import messagebox
import requests
import json
import os


from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("key")


# ------------------------------------------------------
# Function fetches weather data from OpenWeatherMap API
# ------------------------------------------------------
def weather_updates(api_key, city):
    # Sets the base url for the OpenWeatherMap API
    target_url = "https://api.openweathermap.org/data/2.5/weather"
    # A dictionary of parameters for the API request
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        # Sends a get request to the api
        weather_response = requests.get(target_url, params=params)
        # Passes the response content as JSON and stores it in the data variable
        data = weather_response.json()

        # ---------------------------------------------------------------------------------------------------------
        # Condition to check if the HTTP request is succesful and retuns the data. Returns an error message if not
        # ---------------------------------------------------------------------------------------------------------
        if weather_response.status_code == 200:
            return data
        elif weather_response.status_code == 404:
            messagebox.showerror("City not found: {}".format(city))
        else:
            messagebox.showerror("API error: {}".format(data['message']))
            return None
    # ----------------------------------------
    # Handle exception should any error occur
    # ----------------------------------------
    except requests.exceptions.RequestException as e:
        messagebox.showerror(
            "Network error", "An error occured during the request: {}".format(e))
        return None
    except json.JSONDecodeError as e:
        messagebox.showerror("JSON decoding error",
                             "Error decoding json response: {}".format(e))
        return None


# ----------------------------------------------
# Function that takes weather data as parameter
# ----------------------------------------------
def display_updates(weather_data):
    if weather_data:
        result = (
            f"Weather Information:\n"
            f"City: {weather_data['name']}\n"
            f"Temperature: {weather_data['main']['temp']}°C\n"
            f"Weather: {weather_data['weather'][0]['description']}\n"
            f"Wind Speed: {weather_data['wind']['speed']} m/s\n"
            f"Humidity: {weather_data['main']['humidity']}%"
        )
        result_label.config(text=result)
    else:
        result_label.config(text="Unable to fetch weather data.")


# ----------------------------------------------------------
# Function checks for empty/blank city to ensure valid input
# ----------------------------------------------------------
def validate_city(city):
    if not city or not city.strip():
        messagebox.showerror("Error", "Please enter a valid city name.")
        return False
    # if not city.isalpha():
    #     messagebox.showerror("Error", "City name must contain only letters.")
    #     return False
    return True


# ------------------------------------------------------
# Main function that runs after city validation
# ------------------------------------------------------
def get_weather_for_city():
    city = city_entry.get()

    if validate_city(city):
        weather_data = weather_updates(api_key, city)
        display_updates(weather_data)


# -----------------------
# Create the main window
# -----------------------
root = tk.Tk()
root.title("Weather App")

# ---------------
# Adding widgets
# ---------------
city_label = tk.Label(root, text="Enter City:")
city_label.pack(pady=10)

# -------------------
# Entry box for city
# -------------------
city_entry = tk.Entry(root)
city_entry.pack(pady=10)

# ------------------------
# Button to fetch weather
# ------------------------
get_weather_button = tk.Button(
    root, text="Get Weather", command=get_weather_for_city)
get_weather_button.pack(pady=10)

# --------------------------
# Label for weather results
# --------------------------
result_label = tk.Label(root, text="")
result_label.pack(pady=10)


# --------------------------
# Start the main event loop
# --------------------------
root.mainloop()
