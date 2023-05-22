from flask import Flask, request, render_template
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline



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
    if request.method == "POST":
        url = request.form["url"]
        obj = CustomData(url)
        df = obj.get_data_as_dataframe()

        preds = PredictPipeline.predict(df)
        # 1 is safe, -1 is unsafe
        pred = "It is {0:.2f} % safe to go".format(preds[0])
        return render_template('index.html', xx=pred, url=url)
    return render_template("index.html", xx=-1)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
