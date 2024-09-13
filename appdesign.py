#!/usr/bin/env python
# coding: utf-8

# In[1]:


import joblib

try:
    model = joblib.load('solarproject.pkl')
    print("Model loaded successfully.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")


# In[4]:


import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# Set page configuration at the beginning
st.set_page_config(page_title="Solar Power Generation Prediction", layout="wide")

# Load the model
try:
    model = joblib.load('solarproject.pkl') 
    st.write("Model loaded successfully.")
except Exception as e:
    model = None
    st.error(f"An error occurred while loading the model: {e}")

# Function to make predictions
def predict_power_generated(features):
    if model is None:
        st.error("Model is not loaded. Prediction cannot be performed.")
        return None
    
    df = pd.DataFrame([features])
    
    try:
        prediction = model.predict(df)
        return prediction[0]
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        return None

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .header {
            text-align: center;
            color: #333;
            font-size: 2em;
            font-weight: bold;
        }
        .sidebar {
            background-color: #ffebcc;
            padding: 10px;
        }
        .input-box {
            margin: 10px 0;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
        .button:hover {
            background-color: #45a049;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<div class="header">Solar Power Generation Prediction</div>', unsafe_allow_html=True)

# Sidebar with background color and image
st.sidebar.markdown('<div class="sidebar">', unsafe_allow_html=True)
st.sidebar.image('images.jpg', use_column_width=True)  
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Main content
st.write("Enter the environmental variables to predict the solar power generation:")

# User input for the 10 features
col1, col2 = st.columns(2)
with col1:
    distance_to_solar_noon = st.number_input("Distance to Solar Noon (minutes)", key="distance_to_solar_noon")
    temperature = st.number_input("Temperature (°C)", key="temperature")
    wind_direction = st.number_input("Wind Direction (°)", key="wind_direction")
    sky_cover = st.number_input("Sky Cover (oktas)", key="sky_cover")
    humidity = st.number_input("Humidity (%)", key="humidity")

with col2:
    wind_speed = st.number_input("Wind Speed (km/h)", key="wind_speed")
    visibility = st.number_input("Visibility (km)", key="visibility")
    average_wind_speed = st.number_input("Average Wind Speed (km/h)", key="average_wind_speed")
    average_pressure = st.number_input("Average Pressure (hPa)", key="average_pressure")

# Prediction button
if st.button("Predict", key="predict_button"):
    features = {
        "distance-to-solar-noon": distance_to_solar_noon,
        "temperature": temperature,
        "wind-direction": wind_direction,
        "wind-speed": wind_speed,
        "sky-cover": sky_cover,
        "visibility": visibility,
        "humidity": humidity,
        "average-wind-speed-(period)": average_wind_speed,
        "average-pressure-(period)": average_pressure
    }
    
    prediction = predict_power_generated(features)
    
    if prediction is not None:
        st.success(f"Predicted Power Generated: {prediction:.2f} kW")
    else:
        st.error("Prediction could not be made. Please check the model and inputs.")

# Footer
st.markdown('<div class="footer">Developed by Your Name</div>', unsafe_allow_html=True)

