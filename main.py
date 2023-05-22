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

@app.route('/predictdata',methods = ['GET','POST'])
def predict_datapoint():
    if request.method =='GET':
        return render_template('index.html')
    else:
        data = CustomData(url=request.form.get('url'))
        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        result = predict_pipeline.predict(pred_df)
        return render_template('index.html',result = result[0])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
