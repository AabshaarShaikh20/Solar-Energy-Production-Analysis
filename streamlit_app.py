#!/usr/bin/env python
# coding: utf-8

# In[1]:


import joblib

try:
    model = joblib.load('solar.pkl')
    print("Model loaded successfully.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")


# In[2]:


import streamlit as st
import pandas as pd
import joblib

# Loading the model
try:
    model = joblib.load('solar.pkl')  
    st.write("Model loaded successfully.")
except Exception as e:
    model = None
    st.error(f"An error occurred while loading the model: {e}")

# Function to make predictions
def predict_power_generated(features):
    if model is None:
        st.error("Model is not loaded. Prediction cannot be performed.")
        return None
    
    df = pd.DataFrame([features])  # Convert input to DataFrame
    
    try:
        prediction = model.predict(df)
        return prediction[0]
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        return None

# Streamlit app
st.title("Solar Power Generation Prediction")

st.write("Enter the environmental variables to predict the solar power generation:")

# User input
distance_to_solar_noon = st.number_input("Distance to Solar Noon (minutes)")
temperature = st.number_input("Temperature (°C)")
wind_direction = st.number_input("Wind Direction (°)")
wind_speed = st.number_input("Wind Speed (km/h)")
sky_cover = st.number_input("Sky Cover (oktas)")
visibility = st.number_input("Visibility (km)")
humidity = st.number_input("Humidity (%)")
average_wind_speed = st.number_input("Average Wind Speed (km/h)")
average_pressure = st.number_input("Average Pressure (hPa)")

# Prediction button
if st.button("Predict"):
    features = {
        "distance_to_solar_noon": distance_to_solar_noon,
        "temperature": temperature,
        "wind_direction": wind_direction,
        "wind_speed": wind_speed,
        "sky_cover": sky_cover,
        "visibility": visibility,
        "humidity": humidity,
        "average_wind_speed": average_wind_speed,
        "average_pressure": average_pressure
    }
    
    prediction = predict_power_generated(features)
    
    if prediction is not None:
        st.success(f"Predicted Power Generated: {prediction:.2f} kW")
    else:
        st.error("Prediction could not be made. Please check the model and inputs.")

