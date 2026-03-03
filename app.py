import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Cambodia Mangrove Dashboard", layout="wide")
st.title("🌳 Cambodia Mangrove Dashboard")

@st.cache_data
def load_data():
    return gpd.read_file("Cambodia-Mangrove.geojson")

try:
    with st.spinner("Loading geospatial data..."):
        data = load_data()

    # --- CHANGE THIS TO YOUR EXACT QGIS COLUMN NAME ---
    # Example: "PROVINCE", "Name_EN", "ADM1_EN", etc.
    PROVINCE_COLUMN = "YOUR_COLUMN_NAME" 
    
    st.sidebar.header("Dashboard Controls")
    
    # Check if the column exists to prevent crashes
    if PROVINCE_COLUMN in data.columns:
        province_list = ["All Cambodia"] + sorted(data[PROVINCE_COLUMN].dropna().unique().tolist())
        selected_prov = st.sidebar.selectbox("Filter by Province", province_list)
        
        if selected_prov != "All Cambodia":
            display_data = data[data[PROVINCE_COLUMN] == selected_prov]
        else:
            display_data = data
    else:
        st.error(f"Could not find the column '{PROVINCE_COLUMN}'. Please check your spelling!")
        display_data = data # Show everything if it fails

    # Map settings
    bounds = display_data.total_bounds
    center_lat, center_lon = (bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles="CartoDB positron")
    
    folium.GeoJson(
        display_data,
        style_function=lambda x: {'fillColor': '#2E8B57', 'color': '#1f5e3a', 'weight': 1, 'fillOpacity': 0.7}
    ).add_to(m)

    st_folium(m, width="100%", height=600)

except Exception as e:
    st.error("Error loading the dashboard. Please check your files.")
    st.exception(e)
