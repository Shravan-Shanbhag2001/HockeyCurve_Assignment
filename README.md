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

Copy below bash code and execute in cmd(after navigating to folder where u want to create this project):  
git clone <repository-url> cd weather-screener  

2.Install Dependencies  

Navigate to the folder containing your Flask application and Execute the below command to create a virtual environment within this folder:  
python -m venv venv  
This command will create a venv folder inside your project folder. This folder will contain the virtual environment’s files and dependencies.  

Activate the Virtual Environment:

Windows:
Copy below bash code and execute:  
venv\Scripts\activate  

macOS/Linux:  
Copy below bash code and execute 
source venv/bin/activate  

Then install depenencies:  
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

**Finally make sure the project structure looks like this:**  

your_project/  
├── venv/  
├── Backend Code  
├── Frontend Code  
├── Database.py  
├── requirements.txt  
└── other_files/  
**Other files include 'bg_img.jpg' which contains the background image of web page, 'Weather_data.db' which is a database file for testing purpose and it has dummy data from 1st September 2024 to 14 September 2024. Hence while testing put date range within those dates only. **
