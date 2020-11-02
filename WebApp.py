# Import the libraries
import pandas as pd 
import nltk
import torch
from PIL import Image
import streamlit as st

# Create a title and a subtitle
st.write("""
# Diabetes Detection!
Detect if someone has diabetes using machine learning
""")

# Open and display an image in the webapp
image = Image.open('./img/image-23-1.jpg')
# Display the image
st.image(image, caption='ML', use_column_width = True)

# Get the data
# TODO
# Set a subheader
st.subheader('Load data')

# Get the feature input from the user
def get_user_input():
    pregnancies = st.sidebar.slider('pregnancies', 0, 17, 3)

    # Store a dictionary into a variable 
    user_data = {'pregnancies': pregnancies}

    # Transform the data into a data frame

    features = pd.DataFrame(user_data, index = [0])
    return features

# Store the user input into a variable
user_input = get_user_input()

# Set a subheader and display the users input
st.subheader('User input:')
st.write(user_input)

# Create and train the model
# TODO

# Show the model metrics
st.subheader('Model Test Accuracy Score:')
st.write( 'Not implemented yet ')