import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image
import folium
from streamlit_folium import folium_static

def main():
    # Set page config
    st.set_page_config(
        page_title="Taxi Stations Pakistan",
        page_icon="🚖",
        layout="wide"
    )
    
    st.title("🚖 Taxi Station in Pakistan")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Find Taxi Stations", "Upload Image", "Fare Estimator"])
    
    # Page router
    pages = {
        "Home": show_home,
        "Find Taxi Stations": show_map,
        "Upload Image": upload_image,
        "Fare Estimator": fare_estimator
    }
    
    pages[page]()

def show_home():
    st.write("## Welcome to the Taxi Station Finder in Pakistan")
    st.markdown("""
    This application helps you:
    - 📍 Find taxi stations in major Pakistani cities
    - 📸 Upload and process taxi images
    - 💰 Estimate taxi fares
    
    Use the sidebar to navigate through different features!
    """)
    
    # Add some sample statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Stations", "500+", "+5%")
    with col2:
        st.metric("Cities Covered", "5", "+1")
    with col3:
        st.metric("Daily Rides", "10,000+", "+12%")

def show_map():
    st.header("📍 Find Taxi Stations")
    st.write("This map shows taxi stations in major cities of Pakistan.")
    
    # Define major taxi stations
    stations = {
        "Karachi": {
            "coords": (24.8607, 67.0011),
            "stations": "Main Terminal, Airport Stand, Saddar Stand"
        },
        "Lahore": {
            "coords": (31.5497, 74.3436),
            "stations": "Railway Station Stand, Thokar Stand"
        },
        "Islamabad": {
            "coords": (33.6844, 73.0479),
            "stations": "Blue Area Stand, F-8 Stand"
        },
        "Peshawar": {
            "coords": (34.0151, 71.5249),
            "stations": "City Terminal, University Road Stand"
        },
        "Quetta": {
            "coords": (30.1798, 66.9750),
            "stations": "Main Bus Terminal Stand"
        }
    }
    
    # Create map centered on Pakistan
    m = folium.Map(location=[30.3753, 69.3451], zoom_start=6)
    
    # Add markers for each city
    for city, info in stations.items():
        folium.Marker(
            info["coords"],
            popup=f"<b>{city}</b><br>{info['stations']}",
            icon=folium.Icon(color='blue', icon='taxi', prefix='fa')
        ).add_to(m)
    
    folium_static(m)

def upload_image():
    st.header("🖼️ Upload Taxi Image")
    
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Image processing options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Apply Grayscale Filter"):
                img_cv = np.array(image)
                gray_img = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
                st.image(gray_img, caption="Grayscale Image", use_column_width=True)
        
        with col2:
            if st.button("Apply Edge Detection"):
                img_cv = np.array(image)
                gray_img = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
                edges = cv2.Canny(gray_img, 100, 200)
                st.image(edges, caption="Edge Detection", use_column_width=True)

def fare_estimator():
    st.header("💰 Taxi Fare Estimator")
    
    # Input parameters
    col1, col2 = st.columns(2)
    with col1:
        distance = st.number_input("Enter distance (km)", min_value=1, max_value=500, value=10)
        time = st.number_input("Enter estimated time (minutes)", min_value=5, max_value=300, value=30)
    
    with col2:
        peak_hours = st.checkbox("Peak Hours (1.5x fare)")
        ac_vehicle = st.checkbox("AC Vehicle (1.2x fare)")
    
    # Calculate fare
    base_fare = 100  # Base fare in PKR
    rate_per_km = 35  # Per km charge in PKR
    rate_per_min = 2  # Per minute charge in PKR
    
    estimated_fare = base_fare + (distance * rate_per_km) + (time * rate_per_min)
    
    if peak_hours:
        estimated_fare *= 1.5
    if ac_vehicle:
        estimated_fare *= 1.2
    
    # Display fare details
    st.subheader("Fare Breakdown")
    st.write(f"Base Fare: **{base_fare} PKR**")
    st.write(f"Distance Charge: **{distance * rate_per_km} PKR**")
    st.write(f"Time Charge: **{time * rate_per_min} PKR**")
    if peak_hours:
        st.write("Peak Hours Surge: **1.5x**")
    if ac_vehicle:
        st.write("AC Vehicle Premium: **1.2x**")
    
    st.success(f"Total Estimated Fare: **{estimated_fare:.2f} PKR**")

if __name__ == "__main__":
    main()
