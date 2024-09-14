import streamlit as st
import requests
import base64
import pandas as pd
import matplotlib.pyplot as plt

# Defines the list of supported locations
locations = ["New Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru"]
background_image_path = 'bg_img.jpg' #Background image

# Function to encode image to Base64
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encodes image to Base64
encoded_image = encode_image(background_image_path)

# Sets the page title and layout
st.set_page_config(page_title="Weather Screener", page_icon=":sunny:", layout="wide")

# Adds custom CSS for styling the web page
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/jpeg;base64,{encoded_image});
        background-size: cover;
        background-position: center;
    }}
    .header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        text-align: center;
        background-color: #f0f0f0;
        padding: 4.25rem 0px 1rem;
        z-index: 1000;
    }}
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        margin-top: 20px;
        font-size: 14px;
        color: #000;
        z-index: 1000;
    }}
    .main-content {{
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        text-align: center;
        padding-top: 60px;
        padding-bottom: 40px;
    }}
    .main-content h1 {{
        font-size: 28px;
        font-weight: bold;
    }}
    .st-emotion-cache-jkfxgf p {{
        font-size: 20px;
        font-style: italic;
    }}
    .box {{
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
        background-color: #f9f9f9;
        display: flex;
    }}
    .inner-box {{
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
        background-color: #d3d4de;
        flex: 1;
    }}
    .box h3 {{
        text-align: center;
    }}
    .box h2 {{
        text-align: left;
        font-size: small;
    }}
    hr {{
        margin: 0px 0px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Initializes session state to track if button is pressed
if 'button_pressed' not in st.session_state:
    st.session_state['button_pressed'] = False

# Header
st.markdown("<div class='header'><h1>🌞Weather Screener</h1></div>", unsafe_allow_html=True)

# Main content
st.markdown("<div class='main-content'>", unsafe_allow_html=True)
st.markdown("<h1>Welcome to Weather Screener</h1>", unsafe_allow_html=True)

# Search functionality in the main content area
with st.container():
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    selected_location = st.selectbox("Search your location:", locations)
    
    # Date inputs
    st.markdown("<h3>To get weather analysis, enter date range below and press the button.</h3>", unsafe_allow_html=True)
    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')
    
    if st.button("Get Weather Data"):
        st.session_state['button_pressed'] = True  # Mark button as pressed

        # Fetches current weather data
        response = requests.get(f"http://localhost:5000/get-current-weather-data?location={selected_location}")
        
        if response.status_code == 200:
            data = response.json()
            ic = data["weather_icons"]
            
            # Displays current weather data
            with st.container():
                col1, col2 = st.columns([1, 3])
                #Column with all fetched data from backend
                with col1:
                    st.markdown(f"""
                                <div class="box">
                                    <div class="inner-box">
                                        <h3 style="font-size: smaller;">Current Location: 🏙️{selected_location}</h3>
                                        <hr>
                                        <div style="display: flex; align-items: center; justify-content: center;">
                                            <img src="https://openweathermap.org/img/wn/{ic}@2x.png" alt="Example Image" 
                                            width="62" height="62">
                                            <h3 style="font-size: xxx-large"> {data["temperature"]}°C</h3>
                                        </div>
                                        <hr>
                                        <h2> Climate: {data["weather_descriptions"]}</h2>
                                        <hr>
                                        <h2> RealFeel® {data["feelslike"]}°</h2>
                                        <hr>
                                        <h2> Max Temp: {data["temp_max"]}°C</h2>
                                        <hr>
                                        <h2> Min Temp: {data["temp_min"]}°C</h2>
                                        <hr>
                                        <h2> Humidity: {data["humidity"]}%</h2>
                                        <hr>
                                        <h2> Pressure: {data["pressure"]}mb</h2>
                                        <hr>
                                        <h2> Wind Speed: {data["wind_speed"]}m/s</h2>
                                        <hr>
                                        <h2> Wind Degree: {data["wind_degree"]}°</h2>
                                        <hr>
                                        <h2> Visibility: {data["visibility"]}m</h2>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                
                #Contains plots for historical trends of some metrics 
                with col2:
                    col3, col4 = st.columns([1, 1])
                    # Fetch data for the date range
                    start_date_str = start_date.strftime('%d-%m-%Y')
                    end_date_str = end_date.strftime('%d-%m-%Y')

                    response = requests.get(f"http://localhost:5000/get-range_weather-data?start_date={start_date_str}&end_date={end_date_str}")
                    if response.status_code == 200:
                        data = response.json()
                        # Convert to DataFrame and plot
                        df = pd.DataFrame(data)

                        if not df.empty:
                            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
                            # Aggregating data by date
                            df_agg = df.groupby('date').agg({
                                'temperature': 'mean',
                                'humidity': 'mean',
                                'feelslike': 'mean',
                                'pressure': 'mean'
                            }).reset_index()
                            with col3:
                                # Plot temperature trend
                                fig_temp, ax_temp = plt.subplots(figsize=(8, 6))
                                ax_temp.set_xlabel('Date')
                                ax_temp.set_ylabel('Temperature (°C)', color='tab:red')
                                ax_temp.plot(df_agg['date'], df_agg['temperature'], color='tab:red', label='Temperature')
                                ax_temp.tick_params(axis='y', labelcolor='tab:red')
                                ax_temp.set_title('Temperature Trend')
                                plt.tight_layout()
                                st.pyplot(fig_temp)
                                
                                # Plot feels like temperature trend
                                fig_feels_like, ax_feels_like = plt.subplots(figsize=(10, 6))
                                ax_feels_like.set_xlabel('Date')
                                ax_feels_like.set_ylabel('Feels Like Temperature (°C)', color='tab:green')
                                ax_feels_like.plot(df_agg['date'], df_agg['feelslike'], color='tab:green', label='Feels Like Temperature')
                                ax_feels_like.tick_params(axis='y', labelcolor='tab:green')
                                ax_feels_like.set_title('Feels Like Temperature Trend')
                                st.pyplot(fig_feels_like)

                            with col4:
                                # Plot humidity trend
                                fig_humidity, ax_humidity = plt.subplots(figsize=(8, 6))
                                ax_humidity.set_xlabel('Date')
                                ax_humidity.set_ylabel('Humidity (%)', color='tab:blue')
                                ax_humidity.plot(df_agg['date'], df_agg['humidity'], color='tab:blue', label='Humidity')
                                ax_humidity.tick_params(axis='y', labelcolor='tab:blue')
                                ax_humidity.set_title('Humidity Trend')
                                plt.tight_layout()
                                st.pyplot(fig_humidity)
                                
                                # Plot pressure trend
                                fig_pressure, ax_pressure = plt.subplots(figsize=(10, 6))
                                ax_pressure.set_xlabel('Date')
                                ax_pressure.set_ylabel('Pressure (mb)', color='tab:purple')
                                ax_pressure.plot(df_agg['date'], df_agg['pressure'], color='tab:purple', label='Pressure')
                                ax_pressure.tick_params(axis='y', labelcolor='tab:purple')
                                ax_pressure.set_title('Pressure Trend')
                                st.pyplot(fig_pressure)
                        else:
                            st.write("No data available for the selected date range.")
                    else:
                        st.error('Failed to retrieve data')

                # Resets session state after data is displayed
                st.session_state['button_pressed'] = False

# Footer
st.markdown("<div class='footer'>Made By Shravan Shanbhag</div>", unsafe_allow_html=True)
