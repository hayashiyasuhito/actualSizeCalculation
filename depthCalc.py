import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# Function to load data from an uploaded file
@st.cache_data  # Use the new caching method for data
def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    return data

# Set up the title of the app
st.title('Depth calculation for cluster')

# Create a file uploader widget to allow users to upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")


def velocityCalculation(x,fov,screenHeight,settlingSpeed):
    fov_radians = math.radians(fov)
    t_cross = screenHeight/x
    theta = fov_radians * (x / screenHeight) * t_cross
    angular_speed = theta/t_cross
    distance = settlingSpeed/angular_speed
    return distance

if uploaded_file is not None:
    # Load the data
    data = load_data(uploaded_file)

    fov = st.number_input("Input FOV of the Camera", 20.0,90.0)
    focal_length = st.number_input("Input Focul length of the Camera (mm)", 0,100)
    cameraMount = st.selectbox("Vertical or Horisontal",['Vertical','Horisontal'])
    if cameraMount == 'Vertical':
        screenHeight = 1280
    else:
        screenHeight = 720
    settlingSpeed = st.number_input('set settling Velocity', 0.0,5.0)

    velVarianceThreshold = st.number_input('Set threshold of Velocity Variance', 0.00,1.00)
    
    filtered_data = data[data['velocity variance']<velVarianceThreshold]

    filtered_data['distance'] = filtered_data['velocity ave'].apply(velocityCalculation, args = (fov,screenHeight,settlingSpeed))

    filtered_data['actual size'] = filtered_data['length']*filtered_data['distance']/focal_length

    # Checkbox to show the raw data
    if st.checkbox('Show Raw Data'):
        st.write(data)

    if st.checkbox('Show Calculated Distance and actual size'):
        st.write(filtered_data[['distance','length','actual size']])
