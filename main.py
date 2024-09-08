import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from googletrans import Translator
from PIL import Image
import io
import base64
from fpdf import FPDF
import requests
import speech_recognition as sr  # Voice interaction
import pyttsx3  # Text-to-Speech
import folium  # Maps
from streamlit_folium import st_folium  # Folium support for Streamlit
from geopy.geocoders import Nominatim  # Import Nominatim Geocoder
from streamlit_option_menu import option_menu  # For icon support

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Connect to SQLite database
conn = sqlite3.connect('recent_searches.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS searches (id INTEGER PRIMARY KEY, query TEXT, response TEXT)')
conn.commit()

# Translator setup
translator = Translator()

# Voice interaction setup
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("You need to be logged in to access this page.")
        st.stop()
    
    st.title("Main Page")
    st.write("Welcome to the main page!")


# Function to get response from Gemini model
def get_gemini_response(input_text, prompt, image_content=None):
    model = genai.GenerativeModel('gemini-1.5-flash')
    full_input = f"{prompt}\n{input_text}"
    if image_content:
        st.write("Image input is not supported by this model.")
        return "Image input is not supported by this model."
    else:
        response = model.generate_content([full_input])
        return response.text

# Function to handle image upload and conversion
def input_image_setup(uploaded_image):
    if uploaded_image is not None:
        img_byte_arr = io.BytesIO()
        uploaded_image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        image_part = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }
        return image_part
    else:
        return None

# Function to handle voice input
def handle_voice_input():
    with sr.Microphone() as source:
        st.write("Please speak...")
        audio = recognizer.listen(source)
        try:
            input_text = recognizer.recognize_google(audio)
            st.session_state["text_input"] = input_text  # Update the text input
            st.write(f"You said: {input_text}")
        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")
        except sr.RequestError:
            st.write("Sorry, the service is down.")

# Function to save search in database
def save_search(query, response):
    c.execute('INSERT INTO searches (query, response) VALUES (?, ?)', (query, response))
    conn.commit()

# Function to generate a PDF from itinerary
def generate_pdf(itinerary_text, filename="itinerary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add content to PDF
    for line in itinerary_text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True, align='L')

    # Save the PDF to a BytesIO object
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)  # Move to the beginning of the BytesIO stream
    return pdf_output

# Function for real-time data (e.g., weather)
def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def display_rain_chances(data):
    if "rain" in data:
        rain_info = data["rain"]
        if "1h" in rain_info:
            st.write(f"Chance of rain in the next hour: {rain_info['1h']} mm")
        if "3h" in rain_info:
            st.write(f"Chance of rain in the next 3 hours: {rain_info['3h']} mm")
    else:
        st.write("No rain expected.")

# Function to integrate map with Folium
def get_lat_lon(place_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(place_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Function to generate a map
def generate_map(location):
    latitude, longitude = location
    mymap = folium.Map(location=[latitude, longitude], zoom_start=12)
    folium.Marker([latitude, longitude], tooltip="Location").add_to(mymap)
    st_folium(mymap, width=700, height=500)

# Function to get accommodations
def get_accommodations(location):
    if not location:
        return "Please provide a valid location."

    # Generate the prompt based on the user's location
    prompt = f"""
    You should give them the nearby hotels along with the rating based on different sites / or give by different users.
    Hotel name, the address, the contact number, and how much they charge for a basic room. 
    Link directly to the hotel's page, phone number, and a code for 10% off.
    The search location is: {location}
    """

    # Placeholder response (replace this with actual API call or model inference)
    response = f"Searching for accommodations near {location}..."

    # Save the search and response to the database
    c.execute('INSERT INTO searches (query, response) VALUES (?, ?)', (location, response))
    conn.commit()

    return response

# Function to get cafes and restaurants
def get_cafes_restaurants(location):
    if not location:
        return "Please provide a valid location."

    # Google Places API endpoint
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": 1500,  # Search within 1.5km radius
        "type": "restaurant",
        "key": GOOGLE_API_KEY
    }
    
    # Fetch cafes and restaurants
    response = requests.get(endpoint, params=params)
    data = response.json()

    # Process the results
    places = data.get('results', [])
    if not places:
        return "cafes or restaurants found soon."

    results = []
    for place in places:
        name = place.get('name', 'N/A')
        address = place.get('vicinity', 'N/A')
        rating = place.get('rating', 'N/A')
        results.append(f"Name: {name}\nAddress: {address}\nRating: {rating}\n")

    return "\n".join(results)

# Streamlit app configuration
st.title("Virtual Travel Assistant")

# Initialize session state for page if it doesn't exist
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Function to change pages
def change_page(new_page):
    st.session_state.page = new_page

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Map", "Weather", "Recent Info", "Accommodations", "cafes/restaurants"],
        icons=["house", "map", "cloud-sun", "clock-history", "bed", "utensils"],
        menu_icon="cast",
        default_index=0,
    )
    change_page(selected)

# Page content based on selection
if st.session_state.page == "Home":
    st.header("Welcome: your     own personal travel Friend!")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        input_text = st.text_input("Enter a place name or ask for an itinerary:", key="text_input")
    with col2:
        if st.button("🎙", key="voice_input"):
            handle_voice_input()

    uploaded_image = st.file_uploader("Or upload an image of a landmark...", type=["jpg", "jpeg", "png"])
    language = st.radio("Choose response language:", ("English", "Spanish", "Hindi"))

    if st.button("Get Basic Information"):
        if input_text or uploaded_image:
            image_content = None
            if uploaded_image:
                image = Image.open(uploaded_image)
                image_content = input_image_setup(image)

            prompt = """You are an expert in giving information about places. Provide basic, concise information about the place."""
            response = get_gemini_response(input_text, prompt, image_content)

            if language == "Spanish":
                try:
                    response = translator.translate(response, dest='es').text
                except Exception as e:
                    st.error(f"Translation to Spanish failed: {str(e)}")
            elif language == "Hindi":
                try:
                    response = translator.translate(response, dest='hi').text
                except Exception as e:
                    st.error(f"Translation to Hindi failed: {str(e)}")

            st.subheader("Information:")
            st.write(response)

            save_search(input_text or "Uploaded Image", response)
        else:
            st.write("Please enter a place name or upload an image.")

elif st.session_state.page == "Map":
    st.header("Map")
    location = st.text_input("Enter a place name to display on the map:")

    if st.button("Show Map"):
        if location:
            latitude, longitude = get_lat_lon(location)
            if latitude and longitude:
                generate_map((latitude, longitude))
            else:
                st.write("Location not found.")
        else:
            st.write("Please enter a place name.")

elif st.session_state.page == "Weather":
    st.header("Weather Information")
    city_name = st.text_input("Enter city name:")

    if st.button("Get Weather"):
        if city_name:
            weather_data = get_weather(city_name)
            if weather_data:
                st.subheader(f"Weather in {city_name}:")
                st.write(f"Temperature: {weather_data['main']['temp']}°C")
                st.write(f"Weather: {weather_data['weather'][0]['description'].capitalize()}")
                display_rain_chances(weather_data)
            else:
                st.write("Could not retrieve weather information.")
        else:
            st.write("Please enter a city name.")

elif st.session_state.page == "Recent Info":
    st.header("Recent Information")
    st.write("Here are your recent searches:")

    c.execute('SELECT query, response FROM searches ORDER BY id DESC LIMIT 5')
    recent_searches = c.fetchall()

    for search in recent_searches:
        st.subheader(search[0])
        st.write(search[1])

elif st.session_state.page == "Accommodations":
    st.header("Accommodations")
    location = st.text_input("Enter a location for accommodation information:")

    if st.button("Get Accommodations"):
        if location:
            st.write(get_accommodations(location))
        else:
            st.write("Please enter a location.")

elif st.session_state.page == "cafes/restaurants":
    st.header("cafes/restaurants")
    location = st.text_input("Enter a location for nearby cafes or restaurants:")

    if st.button("Get Cafes/Restaurants"):
        if location:
            st.write(get_cafes_restaurants(location))
        else:
            st.write("Please enter a location.")

# Add a download button for the itinerary PDF
if st.session_state.page == "Home" and st.button("Download Itinerary PDF"):
    if input_text:
        itinerary_text = f"Sample itinerary for {input_text}"  # Placeholder for actual itinerary text
        pdf_bytes = generate_pdf(itinerary_text)
        st.download_button(label="Download Itinerary", data=pdf_bytes, file_name="itinerary.pdf")

# Closing SQLite connection when done
conn.close()









if __name__ == "__main__":
    main()
    