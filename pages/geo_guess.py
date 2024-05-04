import streamlit as st
import requests, folium
from streamlit_folium import folium_static

def extract_coordinates(text):
  """Extracts coordinates as a latitude-longitude tuple from a string.

  Args:
      text (str): The text containing the coordinates.

  Returns:
      tuple: A tuple containing latitude (float) and longitude (float),
             or None if coordinates not found.
  """
  lines = text.splitlines()
  for line in lines:
    if line.startswith("Coordinates:"):
      # Extract latitude and longitude (assuming format: "degrees° N/S, degrees° E/W")
      parts = line.split(":")[1].strip().split(",")
      try:
        latitude = float(parts[0].split("°")[0])
        if "S" in parts[0]:
          latitude *= -1  # Convert South to negative value
        longitude = float(parts[1].split("°")[0])
        if "W" in parts[1]:
          longitude *= -1  # Convert West to negative value
        return latitude, longitude
      except ValueError:
        # Handle potential parsing errors (e.g., invalid format)
        return None
  return None  # Coordinates not found in any line

uploaded_file = st.file_uploader('Where the image at?', type=['jpeg','png','jpg'])
if uploaded_file:
    with st.spinner('Waiting for geospy API...'):
        with st.columns(3)[1]:
            st.image(uploaded_file)
        image_formats = {
            'jpeg':'image/jpeg',
            'jpg':'image/jpeg',
            'png':'image/png'
        }
        formData = {'image': (uploaded_file.name.encode('utf-8'), uploaded_file.getbuffer(), image_formats[uploaded_file.name.split('.')[-1]])}
        response = requests.post("https://locate-image-dev-7cs5mab6na-uc.a.run.app/",files=formData)
    data = response.json()
    st.write(data['message'])
    m = folium.Map(location=extract_coordinates(data['message']), zoom_start=12)
    folium.Marker(location=extract_coordinates(data['message'])).add_to(m)
    folium_static(m)
    st.write('---')
    st.write('Supplementary Data:')
    for alt in data['sup_data']:
        st.image(alt['image_link'],caption=alt['image_label'])

