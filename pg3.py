from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from app import app  # Make sure to import the `app` object from your main app file

# Replace the URL below with the raw link to the Starbucks.csv file
csv_url = "https://raw.githubusercontent.com/kkengg/5001AS2_Starbucks/main/Starbucks.csv"

# Read the data
df = pd.read_csv(csv_url)

# Define the layout for pg3
layout = html.Div([
    html.H1("Starbucks Stores Density"),
    dcc.Dropdown(
        id='country-dropdown-pg3',
        options=[{'label': c, 'value': c} for c in df['Country'].unique()],
        value='TH',
        multi=False,
        clearable=False,
    ),
    dcc.Dropdown(
        id='city-dropdown-pg3',
        options=[{'label': c, 'value': c} for c in df['City'].unique()],
        value=['Bangkok', 'Phuket', 'Chiang Mai'],  # Set initial value as a list for multi-selection
        multi=True,  # Enable multi-selection
        clearable=False,
    ),
    dcc.Graph(id='country-map-pg3'),
])

# Define the callback to update the map
@app.callback(
    Output('country-map-pg3', 'figure'),
    Input('country-dropdown-pg3', 'value'),
    Input('city-dropdown-pg3', 'value')
)
def update_map_pg3(selected_country, selected_cities):
    # Filter the data for the selected country and cities
    df_selected = df[(df['Country'] == selected_country) & (df['City'].isin(selected_cities))]

    # Calculate the density of store numbers for each selected city
    city_density = df_selected['City'].value_counts() / df_selected['City'].nunique()
    city_density = city_density.reset_index()
    city_density.columns = ['City', 'Density']

    # Merge the density data with the selected cities' data
    df_selected = df_selected.merge(city_density, on='City')

    # Create the map using scatter_mapbox with bubble size based on store count and custom colors for cities
    fig = px.scatter_mapbox(
        df_selected,
        lat='Latitude',
        lon='Longitude',
        size='Density',  # Use 'Density' column to represent the bubble size (density of store numbers)
        color='City',  # Use 'City' column to represent the color based on cities
        color_discrete_map={'Bangkok': 'red', 'Phuket': 'blue', 'Chiang Mai': 'green'},  # Custom color mapping for cities
        hover_name='Store Name',
        hover_data={'Store Name': True, 'City': True, 'Density': False},  # Exclude density from hover
        zoom=6,  # Adjust the initial zoom level as needed
        mapbox_style='carto-positron',  # Choose the mapbox style (you can try other styles as well)
        title=f'Starbucks Stores in {selected_country} - {", ".join(selected_cities)}',
        height=600
    )

    # Update the map layout
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=df_selected['Latitude'].mean(), lon=df_selected['Longitude'].mean()),
        ),
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return fig
