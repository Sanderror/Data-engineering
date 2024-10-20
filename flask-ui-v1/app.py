# importing Flask and other modules

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
        NumDots = int(request.form.get("NumDots"))  # getting input with name = NumDots in HTML form
        UrlLength = int(request.form.get("UrlLength"))  
        NumDash = int(request.form.get("NumDash"))
        NumDashInHostname = int(request.form.get("NumDashInHostname"))
        AtSymbol = int(request.form.get("AtSymbol"))
        TildeSymbol = int(request.form.get("TildeSymbol"))
        NumUnderscore = int(request.form.get("NumUnderscore"))
        NumPercent = int(request.form.get("NumPercent"))
        NumAmpersand = int(request.form.get("NumAmpersand"))
        NumHash = int(request.form.get("NumHash"))
        NumNumericChars = int(request.form.get("NumNumericChars"))
        NoHttps = int(request.form.get("NoHttps")) # int might not work as it is a binary (yes or no)

        # we will replace this simple (and inaccurate logic) with a prediction from a machine learning model in a
        # future in a future lab
        if UrlLength > 30:
            prediction_value = True
        else:
            prediction_value = False

        return render_template("response_page.html",
                               prediction_variable=prediction_value)

    else:
        return jsonify(message="Method Not Allowed"), 405  # The 405 Method Not Allowed should be used to indicate
    # that our app that does not allow the users to perform any other HTTP method (e.g., PUT and  DELETE) for
    # '/checkdiabetes' path


# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)