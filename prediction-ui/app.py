# importing Flask and other modules
import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify

# Flask constructor
app = Flask(__name__)


# A decorator used to tell the application
# which URL is associated function
@app.route('/checkphishing', methods=["GET", "POST"])
def check_diabetes():
    if request.method == "GET":
        return render_template("input_page.html")

    elif request.method == "POST":
        prediction_input = [
            {
                "NumDots": int(request.form.get("NumDots")),  # getting input with name = NumDots in HTML form
                "UrlLength": int(request.form.get("UrlLength")), 
                "NumDash": int(request.form.get("NumDash")),
                "NumDashInHostname": int(request.form.get("NumDashInHostname")),
                "AtSymbol": int(request.form.get("AtSymbol")),
                "TildeSymbol": int(request.form.get("TildeSymbol")),
                "NumUnderscore": int(request.form.get("NumUnderscore")),
                "NumPercent": int(request.form.get("NumPercent")),
                "NumAmpersand": int(request.form.get("NumAmpersand")),
                "NumHash": int(request.form.get("NumHash")),
                "NumNumericChars": int(request.form.get("NumNumericChars")),
                "NoHttps": int(request.form.get("NoHttps"))
            }
        ]

        logging.debug("Prediction input : %s", prediction_input)

        # use requests library to execute the prediction service API by sending an HTTP POST request
        # use an environment variable to find the value of the diabetes prediction API
        # json.dumps() function will convert a subset of Python objects into a json string.
        # json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary.
        predictor_api_url = os.environ['PREDICTOR_API']
        res = requests.post(predictor_api_url, json=json.loads(json.dumps(prediction_input)))

        prediction_value = res.json()['result']
        logging.info("Prediction Output : %s", prediction_value)
        return render_template("response_page.html",
                               prediction_variable=prediction_value)

    else:
        return jsonify(message="Method Not Allowed"), 405  # The 405 Method Not Allowed should be used to indicate
    # that our app that does not allow the users to perform any other HTTP method (e.g., PUT and  DELETE) for /checkphishing path


# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)