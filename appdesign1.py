#!/usr/bin/env python
# coding: utf-8

# In[6]:


# import joblib

# try:
#     model = joblib.load('solarproject.pkl')
#     print("Model loaded successfully.")
# except Exception as e:
#     print(f"An error occurred while loading the model: {e}")


# In[7]:


import streamlit as st
import pandas as pd
import joblib

# Page config must be the first Streamlit command
st.set_page_config(page_title="Solar Power Generation Prediction", layout="wide")

# Load the model
try:
    model = joblib.load('solarproject.pkl')  # Ensure the correct model file name
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

# Background styling with an image and semi-transparent overlay
st.markdown("""
    <style>
        /* Add background image */
        .background {
            background-image: url('https://www.encstore.com/assets/blogs/1650368737-5-environmental-benefits-of-solar-energy.jpg');
            background-size: cover;
            background-position: center;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.7;  /* Darken the background */
        }

        /* Style for input boxes */
        .stNumberInput > div {
            background-color: #000000;  /* Black background for input box */
            color: #00FF00;  /* Green text for input value */
            border-radius: 5px;
            padding: 10px;
            border: none;
        }

        /* Ensure label text is visible */
        label {
            background-color: rgba(0, 0, 0, 0.7);  /* Semi-transparent black background */
            color: white;  /* White text for labels */
            padding: 5px;
            border-radius: 5px;
        }

        /* Style the output text */
        .stMarkdown h2 {
            background-color: rgba(0, 0, 0, 0.7);  /* Semi-transparent black background for the output */
            color: white;  /* White text for the output */
            padding: 10px;
            border-radius: 5px;
        }

        /* Adjust the alignment of input boxes and labels */
        .stNumberInput input[type="number"] {
            color: #00FF00;  /* Green input text */
            background-color: #000000;  /* Black input field background */
        }

    </style>
""", unsafe_allow_html=True)

# Add background div
st.markdown('<div class="background"></div>', unsafe_allow_html=True)

# Page title
st.title("Solar Power Generation Prediction")

st.write("Enter the environmental variables to predict the solar power generation:")

# Creating the layout with two columns for input fields
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
if st.button("Predict"):
    features = {
        "distance-to-solar-noon": distance_to_solar_noon,
        "temperature": temperature,
        "wind-direction": wind_direction,
        "wind-speed": wind_speed,
        "sky-cover": sky_cover,
        "visibility": visibility,
        "humidity": humidity,
        "average-wind-speed-(period)": average_wind_speed,
        "average-pressure-(period)": average_pressure,
    }

    prediction = predict_power_generated(features)
    
    if prediction is not None:
        st.markdown(f"<h2>Predicted Power Generated: {prediction:.2f} kW</h2>", unsafe_allow_html=True)
    else:
        st.error("Prediction could not be made. Please check the model and inputs.")


# In[ ]:




