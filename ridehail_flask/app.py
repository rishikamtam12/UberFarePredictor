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

@app.route('/comparision')
def comparision():
    # Load the comparison data CSV using the absolute path
    comparision_data = pd.read_csv(os.path.join(STATIC_FOLDER, 'comparision_data.csv'))

    # Convert the DataFrame to an HTML table
    comparision_table = comparision_data.to_html(index=False, classes='table table-striped', border=0)

    # Pass the table to the template
    return render_template('comparision.html', comparision_table=comparision_table)

@app.route('/view-chart/<chart_number>')
def view_chart(chart_number):
    # Define the image paths and descriptions for each pair of charts
    chart_info = {
        '1': {
            'images': ['uber_fare_price_distribution.png', 'lyft_fare_price_distribution.png'],
            'description': 'Visualization 1 - Fare price distribution (histogram and bar plot)'
        },
        '2': {
            'images': ['uber_lyft_distance_price_distribution.png'],
            'description': 'Visualization 2 - Distance vs Price'
        },
        '3': {
            'images': ['uber_heatmap.png', 'lyft_heatmap.png'],
            'description': 'Visualization 3 - Heatmaps [Weather metrics vs Price]'
        },
        '4': {
            'images': ['chart4a.png', 'chart4b.png'],
            'description': 'These charts offer a comparative analysis and visual representation of data distribution.'
        }
    }

    # Get the chart data based on the button clicked
    chart_data = chart_info.get(chart_number, None)

    if not chart_data:
        return 'Chart not found', 404

    # Check if only 1 chart is available in the list
    if len(chart_data['images']) == 1:
        return render_template('view_chart.html', 
                               chart_images=[chart_data['images'][0]], 
                               chart_description=chart_data['description'])
    else:
        # Render the page for multiple charts
        return render_template('view_chart.html', 
                               chart_images=chart_data['images'], 
                               chart_description=chart_data['description'])

if __name__ == "__main__":
    app.run(debug=True)
