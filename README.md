# UberFarePredictor

Predict and analyze rideshare fares for Uber and Lyft with this comprehensive project. Using historical data, weather metrics, and machine learning models, this tool provides insightful visualizations and accurate predictions for ride pricing.

Introduction
Ride fare estimation is a crucial feature for rideshare companies and their users. This project addresses the challenge by building a predictive model that integrates historical ride data with weather information to enhance fare prediction accuracy.

Key Goals:
Enhance Consumer Experience: By providing accurate fare predictions.
Leverage Weather Data: To analyze its influence on pricing.
Visualize Insights: Make data trends accessible and meaningful.
Apply Advanced ML Models: Optimize predictions using cutting-edge techniques.
Features
Data Preprocessing:

Cleaned and integrated rideshare and weather datasets.
Merged ride and weather data using timestamps.
Data Analysis & Visualizations:

Dynamic and static visualizations to explore trends, including:
Fare distribution
Distance vs price relationships
Weather influence on pricing
Hourly pricing patterns
Heatmaps and line charts rendered via Flask.
Machine Learning:

Built models using Random Forest and XGBoost.
Feature engineering for better model accuracy.
Evaluated models using metrics like MAE, MSE, and R².



UberFarePredictor/
├── app.py                # Flask application backend
├── static/               # Static resources (images, CSS, etc.)
├── templates/            # HTML templates for Flask
├── notebooks/            # Jupyter Notebooks for preprocessing and ML modeling
├── data/                 # Sample datasets (rideshare and weather)
├── gcs-connector.jar     # Google Cloud connector for BigQuery integration
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies


Installation and Setup
Prerequisites
Python 3.8 or higher
Google Cloud account with BigQuery API enabled
Steps to Set Up


Clone the Repository:

1. git clone https://github.com/<your-username>/UberFarePredictor.git
   cd UberFarePredictor

2. pip install -r requirements.txt

3. Set Up Google Cloud Credentials:

  Download your service account key file.
  Set the environment variable:
    export GOOGLE_APPLICATION_CREDENTIALS="<path-to-service-key>.json"

4. Run the Application:

    python app.py
   

6. Access the Dashboard:

Open your browser and navigate to http://127.0.0.1:5000.


How to Use

1. Explore Data
Access sample data tables for Uber, Lyft, and weather datasets via the dashboard.

2. View Visualizations
Static Visualizations:
- Predefined charts showing fare distributions, pricing trends, and weather impacts.
Dynamic Visualizations:
- Select source and destination to explore hourly pricing trends.

3. Predict Ride Fares
Input ride details such as distance, source, destination, and weather conditions.
Get predicted fare estimates using advanced machine learning models.

Technologies Used
Backend:
Flask (for web app and API integration)
Google BigQuery (cloud database)
Data Processing:
PySpark (for high-performance data handling)
Pandas (for data analysis)
Machine Learning:
XGBoost
Random Forest
Visualization:
Plotly (dynamic charts)
HTML/JavaScript (interactive visualizations)
Cloud:
Google Cloud Platform (BigQuery and authentication)



This project was developed as part of DS5110 Final Project by Rishi Kamtam and Sabari Mathavan. The integration of machine learning with data visualization highlights the impact of data science on real-world challenges.
  





















