import streamlit as st
import numpy as np
import pickle
from bs4 import BeautifulSoup
from web_scrapping import feature_extraction as fe
from src.Components import model_trainer as ml
import requests as re

import matplotlib.pyplot as plt



app_title = "Content-Based Phishing Website Detection"
app_description = "This ML-based app is developed for Phishing detection. The objective of the app is to detect phishing websites " \
                  "using content data rather than the URL. You can explore the details of the approach, data set, and feature set by clicking on " \
                  "."

# Display the title and additional text
st.title(app_title)
st.write(app_description)



choice = st.selectbox("Decision Tree model is being uused",
                 [
                    'Decision Tree'
                 ]
                )

model = ml.nb_model


if choice == 'Decision Tree':
    model = ml.dt_model
    st.write('DT model is selected!')

url = st.text_input('Enter the URL')
# check the url is valid or not
if st.button('Check!'):
    try:
        response = re.get(url, verify=False, timeout=4)
        if response.status_code != 200:
            print(". HTTP connection was not successful for the URL: ", url)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            vector = [fe.create_vector(soup)]  # it should be 2d array, so I added []
            result = model.predict(vector)
            if result[0] == 0:
                st.success("This web page seems a legitimate!")
                st.balloons()
            else:
                st.warning("Attention! This web page is a potential PHISHING!")
                st.snow()

    except re.exceptions.RequestException as e:
        print("--> ", e)