import streamlit as st
import requests  # Import the requests library
from datetime import datetime

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''
ride_date = st.date_input("Select the date of the ride", value=datetime.now().date())
ride_time = st.time_input("Select the time of the ride", value=datetime.now().time())
pickup_longitude = st.number_input("Pickup Longitude", value=0.0, format="%.6f")
pickup_latitude = st.number_input("Pickup Latitude", value=0.0, format="%.6f")
dropoff_longitude = st.number_input("Dropoff Longitude", value=0.0, format="%.6f")
dropoff_latitude = st.number_input("Dropoff Latitude", value=0.0, format="%.6f")
passenger_count = st.slider("Number of Passengers", min_value=1, max_value=6, value=1)

ride_datetime = datetime.combine(ride_date, ride_time)

# API Le Wagon API
url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':
    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# dictionary with the ride parameters
ride_parameters = {
    "pickup_datetime": ride_datetime.isoformat(),  
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

st.write("### Ride Parameters")
st.json(ride_parameters)

query_string = f"?pickup_datetime={ride_datetime.isoformat()}&pickup_longitude={pickup_longitude}&pickup_latitude={pickup_latitude}&dropoff_longitude={dropoff_longitude}&dropoff_latitude={dropoff_latitude}&passenger_count={passenger_count}"

if st.button("Predict Fare"):
    try:
        # Send a GET request to the API with the ride parameters
        response = requests.get(url + query_string)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response to retrieve the prediction
            prediction = response.json().get("fare", "No prediction available")
            st.success(f"The predicted fare is ${prediction:.2f}")
        else:
            st.error(f"Failed to retrieve prediction. Error code: {response.status_code}")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
