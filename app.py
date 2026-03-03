import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Cambodia Mangroves", layout="wide")
st.title("🌳 Cambodia Mangrove Map")
st.markdown("Visualizing Mangrove Extents and Provincial Boundaries.")

# Load both files from GitHub
@st.cache_data
def load_data():
    mangroves = gpd.read_file("Cambodia-Mangrove.geojson")
    provinces = gpd.read_file("Provinces.geojson")
    return mangroves, provinces

try:
    with st.spinner("Loading map layers..."):
        mangroves, provinces = load_data()

    # Create the base map centered on Cambodia
    m = folium.Map(location=[11.55, 104.91], zoom_start=7, tiles="CartoDB positron")
    
    # 1. Add the Provincial Boundaries (Black outlines, transparent inside)
    folium.GeoJson(
        provinces,
        name="Provincial Boundaries",
        style_function=lambda x: {'fillColor': '#000000', 'color': '#000000', 'weight': 1.5, 'fillOpacity': 0}
    ).add_to(m)

    # 2. Add the Mangroves on top (Green fill)
    folium.GeoJson(
        mangroves,
        name="Mangroves",
        style_function=lambda x: {'fillColor': '#2E8B57', 'color': '#1f5e3a', 'weight': 1, 'fillOpacity': 0.8}
    ).add_to(m)

    # Add a layer control box (Just like QGIS2web!)
    folium.LayerControl(position='topright').add_to(m)

    # Display the map on the webpage
    st_folium(m, width="100%", height=600)

except Exception as e:
    st.error("🚨 Cannot find the files! Please make sure BOTH 'Cambodia-Mangrove.geojson' and 'Provinces.geojson' are uploaded to your GitHub repository.")
