import streamlit as st
import google.generativeai as genai
import json
import numpy as np
import pandas as pd
from datetime import datetime
import requests
import os
from dotenv import load_dotenv  # Required only for local development
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
# Initialize the model
SYSTEM_PROMPT = "You are an AI travel assistant providing structured travel recommendations."
model = genai.GenerativeModel("gemini-2.0-flash-exp", system_instruction=SYSTEM_PROMPT)

def get_travel_recommendation(source, destination, travel_date):
    """Generate AI-based travel recommendations."""
    prompt = f"""
    Plan a trip from {source} to {destination} on {travel_date}.
    Provide estimated prices for each option (Cab, Bus, Train, Flight).
    Format:
    Travel Mode | Duration | Estimated Cost.
    Also, include booking links in the detailed considerations.
    """
    try:
        response = model.generate_content(prompt)
        return response.text if hasattr(response, "text") else "No recommendation available."
    except Exception as e:
        return f"⚠️ Error fetching travel recommendations: {str(e)}"

st.set_page_config(page_title="Explorely AI🧳  - Travel Planner", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #4A90E2;
        }
        .subheader {
            font-size: 24px;
            font-weight: bold;
            color: #333333;
        }
        .travel-option {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="title">Explorely AI🧳 - Your AI Travel Assistant</p>', unsafe_allow_html=True)
st.write("Plan your journey with AI-powered recommendations. ✨")

col1, col2 = st.columns([1, 1])
with col1:
    source = st.text_input("📍 Enter Source Location:")
with col2:
    destination = st.text_input("📍 Enter Destination Location:")
travel_date = st.date_input("📅 Select Travel Date:")

if st.button("🎒   Get Travel Options"):
    if not source or not destination:
        st.warning("⚠️ Please enter both source and destination.")
    elif source.lower() == destination.lower():
        st.error("⚠️ Source and Destination cannot be the same.")
    elif travel_date < datetime.today().date():
        st.error("⚠️ Please select a future travel date.")
    else:
        with st.spinner("Fetching the best travel options... 🚀"):
            travel_recommendation = get_travel_recommendation(source, destination, travel_date)
        
        if "Error" in travel_recommendation:
            st.error(travel_recommendation)  # Display AI error
        else:
            st.subheader("🔮 AI-Generated Travel Recommendations")
            st.write(travel_recommendation)  # Use write instead of markdown
