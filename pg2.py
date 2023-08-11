from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from app import app

# Replace the URL below with the raw link to the Starbucks.csv file
csv_url = "https://raw.githubusercontent.com/kkengg/5001AS2_Starbucks/main/Starbucks.csv"

# Try reading the data with different delimiters
delimiters = [';', '\t', ',']
for delimiter in delimiters:
    try:
        df = pd.read_csv(csv_url, delimiter=delimiter)
        break
    except pd.errors.ParserError:
        continue

# Get the available countries and cities from the DataFrame
available_countries = df['Country'].unique()
available_cities = df['City'].unique()

# Define the layout for pg2
layout = html.Div([
    html.H1("Each Country and Each Number of Starbuck store"),
    dcc.Dropdown(
        id='country-dropdown',
        value=['TH', 'VN', 'MA'],
        multi=True,
        options=[{'label': x, 'value': x} for x in available_countries]
    ),
    dcc.Graph(id='pie-graph'),
    dcc.Graph(id='bar-graph')
])

# Define the callback to update the charts
@app.callback(
    [Output('pie-graph', 'figure'),
     Output('bar-graph', 'figure')],
    [Input('country-dropdown', 'value')]
)
def update_charts(selected_countries):
    df_filtered = df[df['Country'].isin(selected_countries)]

    # Pie Chart
    country_counts = df_filtered['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']
    pie_chart = px.pie(country_counts, values='Count', names='Country', title='Starbucks Stores by Country')

    # Bar Chart
    city_store_counts = df_filtered['City'].value_counts().reset_index()
    city_store_counts.columns = ['City', 'Count of Store Name']
    bar_chart = px.bar(city_store_counts, x='City', y='Count of Store Name', title='Starbucks Stores in Selected Countries')
    bar_chart.update_layout(yaxis_title='Count of Store Name')  # Set y-axis title

    return pie_chart, bar_chart
