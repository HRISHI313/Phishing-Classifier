from flask import Flask, request, render_template
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline
from src.logger import logging
import pandas as pd
import numpy as np
import os
import sys
import pickle
from src.exception import CustomException

application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/predictdata", methods=["GET", "POST"])
def predict_datapoint():
    pred = ""  # Initialize pred with a default value
    if request.method == "POST":
        logging.info('Main-1')
        url = request.form["url"]
        obj = CustomData(url)  # Initialize the CustomData object
        logging.info('Main-2')
        data = obj.get_data_as_dataframe()  # Get data as a dataframe
        logging.info(f'Main-3:{data}')

        # Create an instance of PredictPipeline
        pipeline = PredictPipeline()
        logging.info(f'Main-4:{pipeline}')

        # Call the predict() method on the instance with the 'data' argument
        preds = pipeline.predict(data)
        logging.info(f'Main-5:{preds}')

        if isinstance(preds, np.ndarray) and preds.size > 0:
            prediction_value = preds.item(0)
            percentage = prediction_value * 100
            pred = "There is a {0:.2f}% chance of being safe".format(percentage)
            logging.info(f'Main-6:{pred}')
        else:
            pred = "Unable to make a prediction."

        logging.info(f'Main-6:{pred}')

    return render_template('index.html', results=pred)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
