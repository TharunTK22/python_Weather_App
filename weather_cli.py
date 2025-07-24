import requests
import json

def get_weather(api_key, location):
    """Fetches weather data for a given location."""
    
    # Base URL for the OpenWeatherMap API
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Parameters for the API request
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    
    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        # Parse the JSON response
        weather_data = response.json()
        return weather_data

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Error: City '{location}' not found. Please check the spelling.")
        elif response.status_code == 401:
            print("Error: Invalid API key. Please check your key and try again.")
        else:
            print(f"An HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    except json.JSONDecodeError:
        print("Error: Failed to parse the response from the server.")
        
    return None

def display_weather(data):
    """Formats and displays the weather data."""
    if not data:
        return
        
    # Extract relevant information
    city = data.get('name')
    country = data.get('sys', {}).get('country')
    temp = data.get('main', {}).get('temp')
    humidity = data.get('main', {}).get('humidity')
    description = data.get('weather', [{}])[0].get('description')
    
    if all([city, country, temp, humidity, description]):
        print("\n--- ☀️ Current Weather ---")
        print(f"Location: {city}, {country}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Conditions: {description.title()}")
        print("-------------------------\n")
    else:
        print("Error: Could not retrieve complete weather data.")

def main():
    """Main function to run the weather app CLI."""
    # --- IMPORTANT ---
    # PASTE YOUR API KEY HERE
    API_KEY = "c500db5c1a88d06b2cfce3caa5933ade" 
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Error: Please replace 'YOUR_API_KEY_HERE' with your actual OpenWeatherMap API key.")
        return

    location = input("Enter a city name or ZIP code: ").strip()
    
    if location:
        weather_data = get_weather(API_KEY, location)
        display_weather(weather_data)
    else:
        print("Please enter a location.")
        
    input("\nPress Enter to exit.")

if __name__ == "__main__":
    main()