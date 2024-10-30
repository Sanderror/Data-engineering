# importing Flask and other modules
import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify
import urllib
import re

logging.basicConfig(level=logging.DEBUG)

# Flask constructor
app = Flask(__name__)


# A decorator used to tell the application
# which URL is associated function
@app.route('/checkphishing', methods=["GET", "POST"])
def check_phishing():
    if request.method == "GET":
        return render_template("input_page.html")

    elif request.method == "POST":
        # Obtaining the link as posted in the input form
        input_link = str(request.form.get("Link"))

        # obtain the hostname as a string
        hostname = str(urllib.parse.urlparse(link).hostname)

        # Check if there is a http, if there is, the no_http should be 0, else 1
        http_list = re.findall("^http", link)
        if len(http_list) != 0:
            no_http = 0
        else:
            no_http = 1

        # Get the full prediction input using regular expressions
        prediction_input = [
            {
                "NumDots": int(len(re.findall('\.', input_link))),  # getting input with name = NumDots in HTML form
                "UrlLength": int(len(input_link)), 
                "NumDash": int(len(re.findall('-', input_link))),
                "NumDashInHostname": int(len(re.findall('-', hostname))),
                "AtSymbol": int(len(re.findall('@', input_link))),
                "TildeSymbol": int(len(re.findall('~', input_link))),
                "NumUnderscore": int(len(re.findall('_', input_link))),
                "NumPercent": int(len(re.findall('%', input_link))),
                "NumAmpersand": int(len(re.findall('&', input_link))),
                "NumHash": int(len(re.findall('#', input_link))),
                "NumNumericChars": int(len(re.findall('[0-9]', link))),
                "NoHttps": int(no_http)
            }
        ]
        print("Prediction input: ", prediction_input)
        logging.debug("Prediction input : %s", prediction_input)

        # use requests library to execute the prediction service API by sending an HTTP POST request
        # use an environment variable to find the value of the diabetes prediction API
        # json.dumps() function will convert a subset of Python objects into a json string.
        # json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary.
        predictor_api_url = os.environ['PREDICTOR_API']
        res = requests.post(predictor_api_url, json=json.loads(json.dumps(prediction_input)))
        print("Raw prediction output: ", res)
        prediction_value = res.json()['result']
        print("Prediction output: ", prediction_value)
        logging.info("Prediction Output : %s", prediction_value)
        if prediction_value == "True":
            prediction_value_bool = True
        else:
            prediction_value_bool = False
        return render_template("response_page.html",
                               prediction_variable=prediction_value_bool)

    else:
        return jsonify(message="Method Not Allowed"), 405  # The 405 Method Not Allowed should be used to indicate
    # that our app that does not allow the users to perform any other HTTP method (e.g., PUT and  DELETE) for /checkphishing path


# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
