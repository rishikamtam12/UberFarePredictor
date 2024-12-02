from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

# Dynamically determine the absolute path to the 'static' folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static-visualizations')
def static_visualizations():
    return render_template('static_visualizations.html')

@app.route('/view-sample-data')
def view_sample_data():
    # Load all three CSV files
    lyft_data = pd.read_csv(os.path.join(STATIC_FOLDER, 'lyft_sample_data.csv'))
    uber_data = pd.read_csv(os.path.join(STATIC_FOLDER, 'uber_sample_data.csv'))
    weather_data = pd.read_csv(os.path.join(STATIC_FOLDER, 'weather_sample_data.csv'))

    # Convert DataFrames to HTML tables
    lyft_table = lyft_data.to_html(index=False, classes='table table-striped', border=0)
    uber_table = uber_data.to_html(index=False, classes='table table-striped', border=0)
    weather_table = weather_data.to_html(index=False, classes='table table-striped', border=0)

    # Pass tables to the template
    return render_template('view_sample_data.html', 
                           lyft_table=lyft_table, 
                           uber_table=uber_table, 
                           weather_table=weather_table)

@app.route('/view-chart1')
def view_chart1():
    return render_template('chart1.html')

if __name__ == "__main__":
    app.run(debug=True)
