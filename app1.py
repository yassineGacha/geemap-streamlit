import streamlit as st
import geemap
import ee

# Initialize the Earth Engine module.
ee.Initialize()

# Streamlit App
st.title("Satellite Image Viewer")

# Sidebar for user input
st.sidebar.title("User Input")
start_date = st.sidebar.date_input("Select a start date", value=None)
end_date = st.sidebar.date_input("Select an end date", value=None)
satellite = st.sidebar.selectbox("Select Satellite", ("Landsat 8", "Sentinel-2"))

# Function to get image collection
def get_image_collection(start_date, end_date, satellite):
    if satellite == "Landsat 8":
        collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    elif satellite == "Sentinel-2":
        collection = ee.ImageCollection('COPERNICUS/S2')
    else:
        st.error("Satellite not supported")
        return None

    images = collection.filterDate(start_date, end_date).median()
    return images

# Get image collection based on user input
if start_date and end_date and satellite:
    images = get_image_collection(str(start_date), str(end_date), satellite)
    if images:
        map = geemap.Map(center=[0, 0], zoom=2)
        map.addLayer(images, {}, satellite)
        map.to_streamlit()

st.sidebar.markdown("""
## Instructions
1. Select a start date and an end date.
2. Choose a satellite (Landsat 8 or Sentinel-2).
3. View the satellite image on the map.
""")
