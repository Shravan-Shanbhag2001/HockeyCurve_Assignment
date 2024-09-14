# HockeyCurve_Assignment
Weather data aggregator App

**Weather Screener**  
__Overview_:_  
Weather Screener is a web application that provides weather data and visualizations based on user input. The application includes a Flask backend to fetch and store weather data and a Streamlit frontend to interact with users and display weather information.

**Setup Instructions-**  
Prerequisites:  
Python 3.7 or higher  
Pip (Python package manager)  
SQLite  

**Backend Setup:**  

1.Clone the Repository  

Copy below bash code and execute:  
git clone <repository-url> cd weather-screener  

2.Install Dependencies  

Navigate to the folder containing your Flask application and install the required packages:  

Copy below bash code and execute:  
pip install -r requirements.txt  

3.Initialize the Database  

Ensure the Database.py file is correctly set up to initialize the database. Run the following command:  
python Database.py  
Run the Flask Application  
python app.py  
This will start the Flask server. The API will be available at http://localhost:5000.  

**Frontend Setup:**  

Run the Streamlit Application  
streamlit run app.py  
This will start the Streamlit server. The app will be available at http://localhost:8501.
  
