import streamlit as st 
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 
import requests
from datetime import datetime
import plotly.express as px

#create app title
st.title("Real Time Weather Prediction For Different Towns in Kenya")

#load dataset
df = pd.read_csv("weather_data.csv")

#load trained model
rf_model = joblib.load('Random_Forest_model.pkl')

#api-key for real-time data
api_key = "041e4d657a452be4a5bd985b3d37c801"

#Function to fetch real-time data
def get_weather_data(City):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + City + "&units=metric"
    response = requests.get(complete_url)
    return response.json()

# Real-time Weather Dashboard Section
st.title("Real-Time Weather Dashboard")
city = st.selectbox("Choose a city", ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kericho", 
                                     "Eldoret", "Nyeri", "Meru", "Malindi", "Kajiado",
                                     "Uasin Gishu", "Isiolo", "Nyahururu", "Thika", "Mandera",
                                     "Kisii", "Kapenguria", "Chuka", "Narok",
                                      "Bomet", "Embu", "Bungoma", "Machakos", "Kitui",
                                      "Voi", "Garisa", "Lamu", "Nyamira", "Samburu",
                                      "Maralal", "Lodwar", "Kitale", "Wundanyi", "Mumias",
                                      "Rungiri", "Kabarnet", "Migori", "Siaya", "Homa bay",
                                      "Kakamega", "Busia", "Nandi", "Laikipia", "Taita Taveta",
                                      "Trans Nzioa", "West Pokot", "Tharaka Nithi", "Kiambu", "Marsabit",
                                      "Nyanyuki", "Wote", "Webuye", "Eldama Ravine", "Maua"])
def map_weather_category(description):
    description = description.lower()
    if'clear sky' in description:
        return 'Clear'
    elif 'overcast clouds' in description:
        return 'Cloudy'
    elif 'light rain' in description or 'moderate rain' in description or 'heavy rain' in description:
        return 'Rainy'
    elif 'thunderstorm' in description:
        return 'Stormy'
    else:
        return 'Other'
# Dictionary to map model predictions (e.g., numeric output) to descriptive categories
weather_categories = {0: 'Clear', 1: 'Cloudy', 2: 'Rainy', 3: 'Stormy', 4: 'Other'}
if st.button("Fetch Weather Data"):
    weather_data = get_weather_data(City=city)
    if weather_data["cod"] != "404":
        weather_description = weather_data['weather'][0]['description']

        # Apply the mapping function to get a broader category
        weather_category = map_weather_category(weather_description)
        st.write(f"**City:** {city}")
        st.write(f"**Temperature:** {weather_data['main']['temp']}C")
        st.write(f"**Feels Like:** {weather_data['main']['feels_like']}C")
        st.write(f"**Humidity:** {weather_data['main']['humidity']}%")
        st.write(f"**Wind Speed:** {weather_data['wind']['speed']} m/s")
        st.write(f"**Presure:** {weather_data['main']['pressure']}hPa")
        st.write(f"**Cloudiness:** {weather_data['clouds']['all']} %")
        st.write(f"**Weather Description:** {weather_data['weather'][0]['description']}")
        st.write(f"**Weather Category:** {weather_category}")
    else:
        st.write("City not found!")

# User inputs for weather parameters
Temperature = st.slider("Temperature (°C)", min_value=10, max_value=39, value=25)
Humidity = st.slider("Humidity (%)", min_value=0, max_value=100, value=50)
Pressure = st.slider("Pressure (hPa)", min_value=900, max_value=1100, value=1013)
Wind_Speed = st.slider("Wind Speed (m/s)", min_value=0, max_value=30, value=5)
Cloudiness = st.slider("Cloudiness (%)", min_value=0, max_value=100, value=40)
Feels_Like = st.slider("Feels Like (°C)", min_value=10, max_value=40, value=25)
Temp_Difference = st.slider("Temp_Difference", min_value=-3, max_value=3, value=2)
Humidity_Pressure_Ratio = st.slider("Humidity_Pressure_Ratio", min_value=0.02, max_value=0.08, value=0.05)

# Correct feature names matching those used during model training
Input_data = ['Temperature (C)', 'Feels Like (C)', 'Humidity (%)', 'Pressure (hPa)', 'Wind Speed (m/s)', 'Cloudiness (%)', 'Temp_Difference', 'Humidity_Pressure_Ratio']

# Predict the weather category
if st.button("Predict Weather Category"):
    Weather_Category = pd.DataFrame([[Temperature, Humidity, Pressure, Wind_Speed, Cloudiness, Feels_Like, Temp_Difference, Humidity_Pressure_Ratio]], columns=Input_data)
    prediction = rf_model.predict(Weather_Category)[0]

    prediction_descriptive = weather_categories.get(prediction, "Unknown")
    st.write(f"The predicted weather category is: **{prediction_descriptive}**")

# Example dataframe (replace this with actual historical data)
data = {
    'Date': pd.date_range(start="2023-01-01", periods=30, freq='D'),
    'Temperature': np.random.uniform(low=20, high=35, size=30),
    'Humidity': np.random.uniform(low=50, high=90, size=30)
}
df = pd.DataFrame(data)

# Plot historical temperature and humidity
fig = px.line(df, x='Date', y=['Temperature', 'Humidity'], title="Temperature and Humidity Over Time")
st.plotly_chart(fig)

# Model Performance Section
st.title("Model Performance")
st.write("Metrics evaluating the performance of the trained model:")

accuracy = 0.9 
st.write(f"Model Accuracy: **{accuracy * 100:.2f}%**")

# Downloadable Predictions Section
st.title("Download Weather Predictions")
st.write("Get a downloadable CSV of weather predictions for the selected time period.")
if st.button("Download CSV"):
    csv_data = df.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv_data, file_name="weather_predictions.csv", mime="text/csv")

# Interactive Maps Section
st.title("Weather Map")
st.write("Visualize weather conditions on an interactive map.")

# Define your arrays
latitudes = [
    1.2921, -4.0435, -0.0917, -0.3031, -0.3677, 0.5143, -0.4186, 0.0470, -3.2192, 
    -1.8524, 0.3546, 0.0361, -1.0333, 3.9373, -0.6817, 1.2389, -0.3267, -1.0803, 
    -0.7819, -0.5333, 0.5639, -1.5061, -1.3751, -3.3961, -0.4561, -2.2711, -0.5633, 
    1.0961, 3.1191, 1.0068, -3.4015, 0.3360, 0.4881, -1.0630, 0.0604, -0.5273, 
    0.2827, 0.4601, 0.2131, -1.1741, 2.3383, 0.0101, -1.7801, 0.6007, 0.2371
]
longitudes = [
    36.8219, 39.6682, 34.7679, 36.0800, 35.2833, 35.2698, 36.9513, 37.6496, 40.1169, 
    36.7772, 37.5825, 36.3647, 37.0693, 41.8565, 34.7666, 35.1114, 37.6469, 35.8663, 
    35.3456, 37.4562, 34.5633, 37.2634, 38.0106, 38.5582, 39.6582, 40.9020, 34.9359, 
    36.6999, 35.5961, 35.0053, 38.3572, 34.4881, 35.7433, 34.4730, 34.2881, 34.4577, 
    34.7519, 34.1114, 35.1050, 36.8349, 37.9891, 37.0738, 37.6286, 34.7667, 37.9377
]
cities = [
    'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Kericho', 'Eldoret', 'Nyeri', 'Meru', 'Malindi', 
    'Kajiado', 'Isiolo', 'Nyahururu', 'Thika', 'Mandera', 'Kisii', 'Kapenguria', 'Chuka', 'Narok', 
    'Bomet', 'Embu', 'Bungoma', 'Machakos', 'Kitui', 'Voi', 'Garissa', 'Lamu', 'Nyamira', 
    'Maralal', 'Lodwar','Kitale', 'Wundanyi', 'Mumias', 'Kabarnet', 'Migori', 'Siaya', 'Homa Bay', 
    'Kakamega', 'Busia','Nandi', 'Kiambu', 'Marsabit', 'Nanyuki', 'Wote', 'Webuye', 'Maua'
]
temperatures = [
    17.62, 24.77, 19.32, 16.96, 13.70, 15.06, 16.20, 17.50, 25.00, 
    18.77, 22.23, 14.06, 18.76, 28.89, 14.99, 14.57, 18.21, 16.72, 
    14.76, 18.70, 16.85, 17.97, 18.59, 22.10, 25.22, 25.15, 16.53, 
    17.05, 28.71, 13.49, 16.83, 16.94, 15.52, 17.54, 17.63, 19.92, 
    15.93, 17.89, 20.78, 18.22, 21.88, 16.41, 19.65, 16.60, 18.91
]

# Create the DataFrame
map_data = pd.DataFrame({
    'lat': latitudes,
    'lon': longitudes,
    'City': cities,
    'Temperature': temperatures
})

# Display the map
st.map(map_data)

def get_weather_alerts(lat, lon):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}lat={latitudes}&lon={longitudes}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
city_lat_lon = {
    'Nairobi': (1.2921, 36.8219),
    'Mombasa': (-4.0435, 39.6682),
    'Kisumu': (-0.0917, 34.7679),
    'Nakuru': (-0.3031, 36.0800),
    'Kericho': (-0.3675, 35.2863),
    'Eldoret': (0.5143, 35.2698),
    'Nyeri': (-0.4278, 36.9434),
    'Meru': (0.0463, 37.6559),
    'Malindi': (-3.2184, 40.1169),
    'Kajiado': (-1.8537, 36.7764),
    'Isiolo': (0.3546, 37.5827),
    'Nyahururu': (0.0367, 36.3630),
    'Thika': (-1.0333, 37.0693),
    'Mandera': (3.9366, 41.8670),
    'Kisii': (-0.6838, 34.7716),
    'Kapenguria': (1.2399, 35.1114),
    'Chuka': (-0.3333, 37.6500),
    'Narok': (-1.0875, 35.8660),
    'Bomet': (-0.7893, 35.3419),
    'Embu': (-0.5373, 37.4577),
    'Bungoma': (0.5631, 34.5609),
    'Machakos': (-1.5177, 37.2634),
    'Kitui': (-1.3747, 38.0108),
    'Voi': (-3.3961, 38.5560),
    'Garissa': (-0.4552, 39.6450),
    'Lamu': (-2.2714, 40.9020),
    'Nyamira': (-0.5707, 34.9357),
    'Maralal': (1.0981, 36.7011),
    'Lodwar': (3.1194, 35.5973),
    'Kitale': (1.0157, 35.0063),
    'Wundanyi': (-3.4087, 38.3664),
    'Mumias': (0.3356, 34.4897),
    'Kabarnet': (0.4909, 35.7432),
    'Migori': (-1.0639, 34.4731),
    'Siaya': (0.0607, 34.2877),
    'Homa Bay': (-0.5282, 34.4571),
    'Kakamega': (0.2827, 34.7519),
    'Busia': (0.4605, 34.1116),
    'Nandi': (0.1215, 35.2913),
    'Kiambu': (-1.1720, 36.8344),
    'Marsabit': (2.3382, 37.9900),
    'Nanyuki': (0.0107, 37.0736),
    'Wote': (-1.7807, 37.6284),
    'Webuye': (0.6162, 34.7669),
    'Maua': (0.2307, 37.9309)
}

# Weather Alerts Section
st.title("Weather Alerts")
st.write("Get real-time severe weather warnings or alerts for your location.")

#select a city
city = st.selectbox("Choose a city for weather alerts", list(city_lat_lon.keys()))

if st.button("Get Weather Alerts"):
    lat, lon = city_lat_lon[city]
    weather_data = get_weather_alerts(lat, lon)

    if weather_data and 'alerts' in weather_data:
        alerts = weather_data['alerts']
        st.write(f"**Weather Alerts for {city}:**")

        for alert in alerts:
            st.write(f"- **Event**: {alert['event']}")
            st.write(f"  **Start**: {datetime.utcfromtimestamp(alert['start']).strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"  **End**: {datetime.utcfromtimestamp(alert['end']).strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"  **Description**: {alert['description']}")
            st.write("---")

    else:
        st.write(f"No severe weather alerts for {city} at the moment.")