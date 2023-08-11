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

# Filter the data to include only Starbucks stores in Thailand, Vietnam, and Malaysia
selected_countries = ['TH', 'VN', 'MA']
df_selected = df[df['Country'].isin(selected_countries)]

# Get the count of store names for each country
store_counts = df_selected['Country'].value_counts().reset_index()
store_counts.columns = ['Country', 'Store Count']

# Create a bar chart using Plotly Express
fig = px.bar(store_counts, x='Country', y='Store Count',hover_name='Country', title='Count of Store Starbuck')


layout = html.Div(children=[

      html.H1(children='Count of Starbuck Store'),

        html.Div(children='''
            Country: Thailand, Vietnam and Malaysia.
        '''),

        dcc.Graph(
            id='lineID',
            figure=fig
        ),], style={'padding': 10, 'flex': 1})