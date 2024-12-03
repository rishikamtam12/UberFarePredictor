import os
import pandas as pd
from flask import Flask, render_template, request
from google.cloud import bigquery
from datetime import datetime


# Dynamically determine the absolute path to the 'static' folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/sabarimathavan/Downloads/Python/DS5110/UberFarePredictor/secrets/serviceKey.json'

client = bigquery.Client()
project_id = "idmpproject-441123"
dataset_id = "uberFareEstimation"


app = Flask(__name__)

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
            'description': 'Visualization 1 - Fare price distribution'
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
            'images': ['uber_rainy_condition_prices.png', 'lyft_rainy_condition_prices.png'],
            'description': 'Visualization 4 - Rains influence on price'
        },
        '5': {
            'images': ['uber_hourly_prices.png', 'lyft_hourly_prices.png'],
            'description': 'Visualization 5 - Hourly pricing'
        },
        '6': {
            'images': ['uber_places_hourly_prices.png', 'lyft_places_hourly_prices.png'],
            'description': 'Visualization 6 - Hourly pricing against Places'
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


import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

@app.route('/dynamic-visualizations', methods=['GET', 'POST'])
def dynamic_visualization():
    # Define project_id and dataset_id variables
    project_id = "idmpproject-441123"
    dataset_id = "uberFareEstimation"
    
    # Define the BigQuery queries to get unique sources and destinations from both tables
    source_query = f"""
    SELECT DISTINCT source FROM `{project_id}.{dataset_id}.uber_data`
    UNION DISTINCT
    SELECT DISTINCT source FROM `{project_id}.{dataset_id}.lyft_data`
    """

    destination_query = f"""
    SELECT DISTINCT destination FROM `{project_id}.{dataset_id}.uber_data`
    UNION DISTINCT
    SELECT DISTINCT destination FROM `{project_id}.{dataset_id}.lyft_data`
    """

    # Execute the queries
    sources = client.query(source_query).result()
    destinations = client.query(destination_query).result()

    source_list = [row.source for row in sources]
    destination_list = [row.destination for row in destinations]

    # Create a dictionary mapping sources to possible destinations
    source_to_dest = {}
    for source in source_list:
        query = f"""
        SELECT DISTINCT destination FROM `{project_id}.{dataset_id}.uber_data`
        WHERE source = '{source}'
        UNION DISTINCT
        SELECT DISTINCT destination FROM `{project_id}.{dataset_id}.lyft_data`
        WHERE source = '{source}'
        """
        dest_result = client.query(query).result()
        source_to_dest[source] = [row.destination for row in dest_result]

    # Initialize variables for source and destination
    source = None
    destination = None
    uber_avg_price_per_hour = None
    lyft_avg_price_per_hour = None
    df_html = None  # To store the HTML table

    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')

        # BigQuery query to get the data based on selected source and destination from both tables
        query = f"""
        WITH uber_data AS (
            SELECT 
                EXTRACT(HOUR FROM time_stamp) AS hour, 
                ROUND(AVG(price), 2) AS avg_price
            FROM `{project_id}.{dataset_id}.uber_data`
            WHERE source = '{source}' AND destination = '{destination}'
            GROUP BY hour
        ),
        lyft_data AS (
            SELECT 
                EXTRACT(HOUR FROM time_stamp) AS hour, 
                ROUND(AVG(price), 2) AS avg_price
            FROM `{project_id}.{dataset_id}.lyft_data`
            WHERE source = '{source}' AND destination = '{destination}'
            GROUP BY hour
        )
        SELECT 
            COALESCE(u.hour, l.hour) AS hour,
            u.avg_price AS uber_avg_price,
            l.avg_price AS lyft_avg_price
        FROM uber_data u
        FULL OUTER JOIN lyft_data l ON u.hour = l.hour
        ORDER BY hour
        """
        
        # Execute the query and fetch the results
        result = client.query(query).result()

        # Convert the result to a DataFrame
        df = pd.DataFrame([dict(row) for row in result])

        if df.empty:
            uber_avg_price_per_hour = "No data available for the selected source and destination."
            lyft_avg_price_per_hour = "No data available for the selected source and destination."
        else:
            # Plot the line graph
            fig = go.Figure()

            fig.add_trace(go.Scatter(x=df['hour'], y=df['uber_avg_price'], mode='lines', name='Uber'))
            fig.add_trace(go.Scatter(x=df['hour'], y=df['lyft_avg_price'], mode='lines', name='Lyft'))

            # Set the range for the x-axis and y-axis
            fig.update_layout(
                title="Uber vs Lyft Average Price Per Hour",
                xaxis_title="Hour",
                yaxis_title="Average Price",
                xaxis=dict(
                    range=[df['hour'].min(), df['hour'].max()]  # Limit x-axis range to the hours in the data
                ),
                yaxis=dict(
                    range=[df[['uber_avg_price', 'lyft_avg_price']].min().min(), df[['uber_avg_price', 'lyft_avg_price']].max().max()]  # Adjust y-axis range dynamically
                )
            )

            # Render the plot in the HTML template
            graph_html = fig.to_html(full_html=False)

            # Convert the DataFrame to an HTML table
            df_html = df.to_html(classes='data', header=True, index=False)
            uber_avg_price_per_hour = graph_html  # Ensure this contains the full HTML of the graph

    return render_template('dynamic_visualizations.html', 
                           sources=source_list, 
                           destinations=destination_list, 
                           source_to_dest=source_to_dest, 
                           uber_avg_price_per_hour=uber_avg_price_per_hour,
                           df_html=df_html, 
                           selected_source=source,
                           selected_destination=destination)    
    
if __name__ == "__main__":
    app.run(debug=True)
