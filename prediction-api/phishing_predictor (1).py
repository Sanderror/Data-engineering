import json
import os

import pandas as pd
from flask import jsonify
#from keras.models import load_model
import logging
from io import StringIO
import pickle


class PhishingPredictor:
    def __init__(self):
        self.model = None

    def predict_single_record(self, prediction_input):
        logging.debug(prediction_input)
        if self.model is None:
            try:
                model_repo = os.environ['MODEL_REPO']
                #file_path = os.path.join(model_repo, "model.h5")
                #self.model = load_model(file_path)
                with open('model-A1-v3.pkl', 'rb') as file:
                    self.model = pickle.load(file)
            except KeyError:
                print("MODEL_REPO is undefined")
                #self.model = load_model('model.h5')
                with open('model-A1-v3.pkl', 'rb') as file:
                    self.model = pickle.load(file)

        df = pd.read_json(StringIO(json.dumps(prediction_input)), orient='records')
        print("Dataframe: ", df)
        y_pred = self.model.predict(df)
        print("Y prediction: ", y_pred)
        logging.info(y_pred[0])
        status = (y_pred[0] > 0.5)
        print("Y prediction status: ", status)
        logging.info(type(status))
        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        return jsonify({'result': str(status)}), 200
