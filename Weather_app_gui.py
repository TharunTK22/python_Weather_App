import tkinter as tk
from tkinter import messagebox, font
import requests
from PIL import Image, ImageTk
import io

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        
        # --- IMPORTANT ---
        # PASTE YOUR API KEY HERE
        self.api_key = "c500db5c1a88d06b2cfce3caa5933ade"
        
        # --- UI Elements ---
        self.location_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="metric") # 'metric' for Celsius, 'imperial' for Fahrenheit

        self.create_widgets()

    def create_widgets(self):
        # Custom fonts
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        label_font = font.Font(family="Helvetica", size=12)
        info_font = font.Font(family="Helvetica", size=14, weight="bold")

        # Top Frame for input
        top_frame = tk.Frame(self.root, bg="#3498db", pady=10)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="Enter Location:", bg="#3498db", fg="white", font=label_font).pack(side="left", padx=10)
        location_entry = tk.Entry(top_frame, textvariable=self.location_var, font=label_font, width=15)
        location_entry.pack(side="left", padx=5)
        location_entry.bind("<Return>", self.get_weather_event) # Bind Enter key

        search_button = tk.Button(top_frame, text="Get Weather", command=self.get_weather, font=label_font)
        search_button.pack(side="left", padx=10)

        # Weather Info Frame
        self.weather_frame = tk.Frame(self.root)
        self.weather_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.location_label = tk.Label(self.weather_frame, text="", font=title_font)
        self.location_label.pack(pady=5)

        self.icon_label = tk.Label(self.weather_frame)
        self.icon_label.pack()

        self.temp_label = tk.Label(self.weather_frame, text="", font=info_font)
        self.temp_label.pack()

        self.desc_label = tk.Label(self.weather_frame, text="", font=label_font)
        self.desc_label.pack()
        
        self.details_label = tk.Label(self.weather_frame, text="", font=label_font)
        self.details_label.pack(pady=10)

        # Unit conversion buttons
        unit_frame = tk.Frame(self.root, pady=10)
        unit_frame.pack()
        tk.Radiobutton(unit_frame, text="Celsius (°C)", variable=self.unit_var, value="metric", command=self.get_weather).pack(side="left")
        tk.Radiobutton(unit_frame, text="Fahrenheit (°F)", variable=self.unit_var, value="imperial", command=self.get_weather).pack(side="left")

    def get_weather_event(self, event):
        """Handler for Enter key event."""
        self.get_weather()

    def get_weather(self):
        location = self.location_var.get().strip()
        if not location:
            messagebox.showwarning("Input Error", "Please enter a location.")
            return

        if self.api_key == "YOUR_API_KEY_HERE":
            messagebox.showerror("API Key Error", "Please replace 'YOUR_API_KEY_HERE' with your actual OpenWeatherMap API key in the code.")
            return

        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': location,
            'appid': self.api_key,
            'units': self.unit_var.get()
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            self.display_weather(data)
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                messagebox.showerror("Error", f"City '{location}' not found.")
            elif response.status_code == 401:
                messagebox.showerror("API Key Error", "Invalid API key provided.")
            else:
                messagebox.showerror("Error", f"An HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            messagebox.showerror("Error", f"A network error occurred: {err}")

    def display_weather(self, data):
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        description = data['weather'][0]['description'].title()
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        icon_code = data['weather'][0]['icon']

        self.location_label.config(text=f"{city}, {country}")
        
        temp_unit = "°C" if self.unit_var.get() == "metric" else "°F"
        self.temp_label.config(text=f"{temp:.1f}{temp_unit}")
        self.desc_label.config(text=description)
        
        details = f"Humidity: {humidity}%  |  Wind Speed: {wind_speed} "
        details += "m/s" if self.unit_var.get() == "metric" else "mph"
        self.details_label.config(text=details)

        # Get and display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            icon_response = requests.get(icon_url)
            icon_data = icon_response.content
            image = Image.open(io.BytesIO(icon_data))
            self.weather_icon = ImageTk.PhotoImage(image)
            self.icon_label.config(image=self.weather_icon)
        except Exception as e:
            print(f"Could not load weather icon: {e}")
            self.icon_label.config(image='') # Clear image if it fails

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()