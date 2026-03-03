import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Cambodia Mangrove Map", layout="wide")
st.title("🌳 Cambodia Mangrove Map")
st.markdown("Visualizing Mangroves and Provincial Boundaries.")

@st.cache_data
def load_data():
    # Load BOTH files
    mangroves = gpd.read_file("Cambodia-Mangrove.geojson")
    provinces = gpd.read_file("Provinces.geojson")
    return mangroves, provinces

try:
    with st.spinner("Loading map layers..."):
        mangroves, provinces = load_data()

    # Create the base map
    m = folium.Map(location=[11.55, 104.91], zoom_start=7, tiles="CartoDB positron")
    
    # 1. Add the Provincial Boundaries (Black outlines, transparent inside)
    folium.GeoJson(
        provinces,
        name="Provinces",
        style_function=lambda x: {'fillColor': 'none', 'color': 'black', 'weight': 1.5}
    ).add_to(m)

    # 2. Add the Mangroves on top (Green fill)
    folium.GeoJson(
        mangroves,
        name="Mangroves",
        style_function=lambda x: {'fillColor': '#2E8B57', 'color': '#1f5e3a', 'weight': 1, 'fillOpacity': 0.8}
    ).add_to(m)

    # Add a layer control box so users can turn them on/off
    folium.LayerControl().add_to(m)

    # Display the map
    st_folium(m, width="100%", height=600)

except Exception as e:
    st.error("🚨 Missing files! Make sure BOTH 'Cambodia-Mangrove.geojson' and 'Provinces.geojson' are uploaded to GitHub.")
