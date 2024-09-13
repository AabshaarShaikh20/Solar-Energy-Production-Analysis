#!/usr/bin/env python
# coding: utf-8

# In[1]:


import joblib

try:
    model = joblib.load('solarproject.pkl')
    print("Model loaded successfully.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")


# In[2]:


import streamlit as st
import pandas as pd
import joblib
import base64

# Function to set a background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
    st.markdown(bg_img, unsafe_allow_html=True)

# Adding background image
add_bg_from_local('images.jpg')  

# Load the model
try:
    model = joblib.load('solarproject.pkl')  #
    st.write("<h2 style='color: white;'>Model loaded successfully.</h2>", unsafe_allow_html=True)
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

# Streamlit app header
st.markdown("<h1 style='text-align: center; color: white;'>Solar Power Generation Prediction</h1>", unsafe_allow_html=True)

st.write("<p style='text-align: center; color: white;'>Enter the environmental variables to predict the solar power generation:</p>", unsafe_allow_html=True)

# Input form with styled button
with st.form("prediction_form"):
    distance_to_solar_noon = st.number_input("Distance to Solar Noon (minutes)", key="solar_noon")
    sky_cover = st.number_input("Sky Cover (oktas)", key="sky_cover")
    humidity = st.number_input("Humidity (%)", key="humidity")
    wind_direction = st.number_input("Wind Direction (°)", key="wind_direction")
    wind_speed = st.number_input("Wind Speed (km/h)", key="wind_speed")
    temperature = st.number_input("Temperature (°C)", key="temperature")
    visibility = st.number_input("Visibility (km)", key="visibility")
    average_wind_speed_period = st.number_input("Average Wind Speed (km/h)", key="avg_wind_speed")
    average_pressure_period = st.number_input("Average Pressure (hPa)", key="avg_pressure")
    
    # Create a button with a custom style
    submit_button = st.form_submit_button(label="Predict", 
                                          help="Click to predict the solar power generation",
                                          use_container_width=True)

    # When the form is submitted
    if submit_button:
        features = {
            "distance-to-solar-noon": distance_to_solar_noon,
            "temperature": temperature,
            "wind-direction": wind_direction,
            "wind-speed": wind_speed,
            "sky-cover": sky_cover,
            "visibility": visibility,
            "humidity": humidity,
            "average-wind-speed-(period)": average_wind_speed_period,
            "average-pressure-(period)": average_pressure_period,
        }
        prediction = predict_power_generated(features)

        if prediction is not None:
            st.success(f"Predicted Power Generated: {prediction:.2f} kW")
        else:
            st.error("Prediction could not be made. Please check the model and inputs.")

# Custom CSS for button styles
st.markdown("""
    <style>
    .stButton button {
        color: white;
        background-color: #4CAF50;
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
        border-radius: 8px;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

