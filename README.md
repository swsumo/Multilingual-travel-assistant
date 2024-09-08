# Multilingual-travel-assistant

This is a powerful tool designed to provide real-time travel guidance, destination information, personalized recommendations, and more. Built using cutting-edge technologies, this assistant can help you plan your travels, get weather updates, view maps, and even locate the best cafes and restaurants based on your preferences.
Features Destination Information: Get detailed information about any place, including nearby attractions and important landmarks. Weather Updates: Receive real-time weather information for your destination. Interactive Map: View maps to help you navigate your chosen destination. Recent Searches: Easily access a history of your recent searches. Itinerary Planning: Generate and download a personalized itinerary in PDF format for the duration of your stay. Cafes/Restaurants Locator: Find the best cafes and restaurants near you, based on your location and preferences. Technologies Used Google Gemini Model: Used for natural language understanding and generating intelligent responses. Streamlit: Serves as the frontend for the application, providing a simple and interactive user interface. pyttsx3: A text-to-speech conversion library used for audio feedback. geopy (Nominatim): A library for geocoding and locating geographical coordinates. Google Translate (Translator): Enables multilingual support, translating text into various languages. API Keys To use this application, the following API keys are required:

Google API Key: Used for integrating Google services such as the Gemini model. OpenWeather API Key: Provides access to real-time weather data.

A brief description of what this project does and who it's for


## API Reference

### GOOGLE API KEY FOR GEMINI MODEL WHICH WILL BE USED.

```http
import os
google_api_key = os.getenv('GOOGLE_API_KEY')

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `GOOGLE_API_KEY` | `string` | **Required**. You can find the documentation and details for the specific Google API services you are using. |

### OPEN WEATHER KEY TO GET LIVE UPDATES ABT WEATHER.



```http
import os
openweather_api_key = os.getenv('OPENWEATHER_API_KEY')

```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `OPENWEATHER_API_KEY`      | `string` | **Required**.  You can find the official documentation in OpenWeather API Documentation
|




## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

GOOGLE_API_KEY


OPENWEATHER_API_KEY


streamlit 

google-auth 

google-auth-oauthlib 

google-auth-httplib2

google-api-python-client 

google.generativeai 

python-dotenv 

pillow

googletrans 
