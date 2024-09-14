#!/usr/bin/env python
# coding: utf-8

# In[1]:


import joblib

try:
    model = joblib.load('solarproject.pkl')
    print("Model loaded successfully.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")


# In[ ]:


import streamlit as st
import pandas as pd
import joblib

# Set the page configuration and background image
st.set_page_config(page_title="Solar Power Generation Prediction", layout="wide")

# Define the CSS style for custom background and input styles
st.markdown(
    f"""
    <style>
    /* Set background image */
    .stApp {{
        background-image: url('https://www.encstore.com/assets/blogs/1650368737-5-environmental-benefits-of-solar-energy.jpg');
        background-size: cover;
        background-position: center;
    }}

    /* Customize the input box */
    .input-box {{
        background-color: black;
        border: 2px solid green;
        padding: 10px;
        border-radius: 5px;
        color: green;
        font-weight: bold;
        width: 100%;
        box-sizing: border-box;
    }}
    
    /* Adjust the text color for the labels */
    label {{
        color: white;
        font-size: 18px;
    }}
    
    /* Adjust the prediction button */
    .stButton>button {{
        background-color: green;
        color: white;
        border-radius: 5px;
        width: 100px;
        height: 40px;
        font-size: 16px;
        font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

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

# Streamlit app title
st.title("Solar Power Generation Prediction")

st.write("Enter the environmental variables to predict the solar power generation:")

# User input for features with customized input boxes
distance_to_solar_noon = st.number_input("Distance to Solar Noon (minutes)", format="%.2f", step=0.01, key="distance_to_solar_noon")
sky_cover = st.number_input("Sky Cover (oktas)", format="%.2f", step=0.01, key="sky_cover")
humidity = st.number_input("Humidity (%)", format="%.2f", step=0.01, key="humidity")
wind_direction = st.number_input("Wind Direction (°)", format="%.2f", step=0.01, key="wind_direction")
wind_speed = st.number_input("Wind Speed (km/h)", format="%.2f", step=0.01, key="wind_speed")
temperature = st.number_input("Temperature (°C)", format="%.2f", step=0.01, key="temperature")
visibility = st.number_input("Visibility (km)", format="%.2f", step=0.01, key="visibility")
average_wind_speed = st.number_input("Average Wind Speed (km/h)", format="%.2f", step=0.01, key="average_wind_speed")
average_pressure = st.number_input("Average Pressure (hPa)", format="%.2f", step=0.01, key="average_pressure")

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
        st.success(f"Predicted Power Generated: {prediction:.2f} kW")
    else:
        st.error("Prediction could not be made. Please check the model and inputs.")

