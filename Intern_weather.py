import tkinter as tk
from tkinter import ttk
import requests
from geopy import Nominatim
import geocoder

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        self.location_label = ttk.Label(root, text="Location:")
        self.location_entry = ttk.Entry(root, width=30)

        self.search_button = ttk.Button(root, text="Search", command=self.get_weather)
        self.use_gps_button = ttk.Button(root, text="Use GPS", command=self.get_location_from_gps)

        self.result_label = ttk.Label(root, text="")
        self.weather_icon_label = ttk.Label(root, text="")
        
        self.location_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.location_entry.grid(row=0, column=1, padx=10, pady=10)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)
        self.use_gps_button.grid(row=0, column=3, padx=10, pady=10)
        self.result_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        self.weather_icon_label.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    def get_weather(self):
        location = self.location_entry.get()
        if not location:
            return

        data = self.fetch_weather_data(location)
        if data:
            self.display_weather(data)
        else:
            self.result_label.config(text="Error fetching data")

    def get_location_from_gps(self):
        location = self.get_user_location()
        if location:
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, location)

    def fetch_weather_data(self, location):
        # api_key = "YOUR_API_KEY"  # Replace with your actual API key
        api_url = f"http://api.weatherapi.com/v1/current.json?key=563020710a8e4fd18bd112204232609&q={location}&aqi=no"

        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def display_weather(self, data):
        location_info = data.get('location', {})
        current_info = data.get('current', {})
        condition_info = current_info.get('condition', {})

        location_str = f"{location_info.get('name', '')}, {location_info.get('region', '')}, {location_info.get('country', '')}"
        temperature_str = f"Temperature: {current_info.get('temp_c', '')}°C ({current_info.get('temp_f', '')}°F)"
        condition_str = f"Condition: {condition_info.get('text', '')}"
        wind_str = f"Wind: {current_info.get('wind_kph', '')} kph, {current_info.get('wind_dir', '')}"
        humidity_str = f"Humidity: {current_info.get('humidity', '')}%"

        self.result_label.config(text=f"{location_str}\n{temperature_str}\n{condition_str}\n{wind_str}\n{humidity_str}")

        # Display weather icon
        icon_url = f"https:{condition_info.get('icon', '')}"
        icon_response = requests.get(icon_url)
        if icon_response.status_code == 200:
            icon_data = tk.PhotoImage(data=icon_response.content)
            self.weather_icon_label.config(image=icon_data)
            self.weather_icon_label.image = icon_data
        else:
            self.weather_icon_label.config(text="Icon not available")

    def get_user_location(self):
        # Try to get user's location using GPS coordinates
        g = geocoder.ip('me')
        if g.latlng:
            geolocator = Nominatim(user_agent="weather_app")
            location = geolocator.reverse(g.latlng, language='en')
            return location.address
        else:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
