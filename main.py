from flask import Flask, request, render_template
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

import pandas as pd
import numpy as np
import sys

from src.exception import CustomException

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            url = request.form.get('url')
            data = CustomData(url=url)
            pred_df = data.get_data_as_data_frame()
            print(pred_df)

            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)

            return render_template('index.html', results=results)
        except Exception as e:
            # You can handle the exception here or log it
            raise CustomException(e, sys)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
