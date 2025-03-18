# Ocean Station Plotter 
# Mak Saito 2025
import streamlit as st
import plotly.express as px
import pandas as pd

def standard_to_decimal(degrees, minutes, seconds, direction):
    decimal = degrees + (minutes / 60) + (seconds / 3600)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def plot_coordinates(coord_type, latitudes, longitudes, show_gridlines, land_color, sea_color, show_rivers_lakes):
    if coord_type == 'd':
        latitudes = [float(lat) for lat in latitudes.split(',')]
        longitudes = [float(lon) for lon in longitudes.split(',')]
    elif coord_type == 's':
        lat_deg = latitudes.split(',')
        lon_deg = longitudes.split(',')
        lat_min = st.session_state['lat_min'].split(',')
        lat_sec = st.session_state['lat_sec'].split(',')
        lon_min = st.session_state['lon_min'].split(',')
        lon_sec = st.session_state['lon_sec'].split(',')

        latitudes = []
        longitudes = []
        for i in range(len(lat_deg)):
            if lat_deg[i][-1] not in ['N', 'S'] or lon_deg[i][-1] not in ['E', 'W']:
                st.error("Please add N, S, E, or W to the degrees for latitude and longitude.")
                return
            lat_direction = lat_deg[i][-1]
            lon_direction = lon_deg[i][-1]
            lat_deg_value = int(lat_deg[i][:-1])
            lon_deg_value = int(lon_deg[i][:-1])
            lat_min_value = int(lat_min[i]) if lat_min[i] else 0
            lat_sec_value = float(lat_sec[i]) if lat_sec[i] else 0.0
            lon_min_value = int(lon_min[i]) if lon_min[i] else 0
            lon_sec_value = float(lon_sec[i]) if lon_sec[i] else 0.0
            latitudes.append(standard_to_decimal(lat_deg_value, lat_min_value, lat_sec_value, lat_direction))
            longitudes.append(standard_to_decimal(lon_deg_value, lon_min_value, lon_sec_value, lon_direction))

    fig = px.scatter_geo(lat=latitudes, lon=longitudes)
    fig.update_layout(title="Station Map Coordinate Checker", geo_scope='world')
    
    # Add latitude and longitude tick marks to the map
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor=land_color,
        showocean=True,
        oceancolor=sea_color,
        showlakes=show_rivers_lakes,
        lakecolor="Blue",
        showrivers=show_rivers_lakes,
        rivercolor="Blue",
        lataxis_showgrid=show_gridlines,
        lonaxis_showgrid=show_gridlines,
        lataxis_gridcolor="Grey",
        lonaxis_gridcolor="Grey"
    )
    
    st.plotly_chart(fig)

    show_table(latitudes, longitudes)

def show_table(latitudes, longitudes):
    table_data = {'Latitude (Decimal)': latitudes, 'Longitude (Decimal)': longitudes}
    df = pd.DataFrame(table_data)
    df.index += 1
    df.index.name = 'Station'
    st.table(df)

st.title("Ocean Station Mapper")
st.write("Ocean station coordinates plotter and conversion calculator - Beta Version")
st.write("For multiple stations, place a comma between coordinates")

coord_type = st.selectbox("Select coordinate type:", ["Decimal", "DMS (degrees, minutes, seconds)"])

if coord_type == "Decimal":
    lat_decimal = st.text_input("Enter latitudes in decimal (comma separated, up to 50):")
    lon_decimal = st.text_input("Enter longitudes in decimal (comma separated, up to 50):")
elif coord_type == "DMS (degrees, minutes, seconds)":
    lat_deg = st.text_input("Enter latitude degrees with optional hemisphere suffix (N, S) (comma separated, up to 50):")
    lat_min = st.text_input("Enter latitude minutes (comma separated, up to 50):", key='lat_min')
    lat_sec = st.text_input("Enter latitude seconds (comma separated, up to 50):", key='lat_sec')
    lon_deg = st.text_input("Enter longitude degrees with optional hemisphere suffix (E, W) (comma separated, up to 50):")
    lon_min = st.text_input("Enter longitude minutes (comma separated, up to 50):", key='lon_min')
    lon_sec = st.text_input("Enter longitude seconds (comma separated, up to 50):", key='lon_sec')

show_gridlines = st.selectbox("Show Gridlines:", [True, False], index=1)
land_color = st.color_picker("Pick Land Color:", "#646419")  # Default color: #646419
sea_color = st.color_picker("Pick Sea Color:", "#FFFFFF")   # Default color: White

show_rivers_lakes = st.checkbox("Show Major Rivers and Lakes", value=False)

if st.button("Plot Coordinates"):
    if coord_type == "Decimal":
        plot_coordinates('d', lat_decimal, lon_decimal, show_gridlines, land_color, sea_color, show_rivers_lakes)
    elif coord_type == "DMS (degrees, minutes, seconds)":
        plot_coordinates('s', lat_deg, lon_deg, show_gridlines, land_color, sea_color, show_rivers_lakes)

st.write("Report errors send message to msaito@whoi.edu, Updated March 2025")
