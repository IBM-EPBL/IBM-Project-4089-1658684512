import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
# importing the inputScript file used to analyze the URL
import InputScript
from fjagepy import Gateway


# load model
app = Flask(__name__, template_folder='template')
model = pickle.load(open(
    "Phishing_Website.pkl", 'rb'))


@app.route('/')
# def helloworld():
#     return render_template("index.html")
# Redirects to the page to give the user input URL.
@app.route('/predict')
def predict():
    # client_token = Gateway.generate_client_token.generate_client_token()
    return render_template('index.html')

# Fetches the URL given by the URL and passes to inputScript


@ app.route('/y_predict', methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    url = request.form['URL']
    checkprediction = InputScript.main(url)
    print(checkprediction)
    prediction = model.predict(checkprediction)
    print(prediction)
    output = prediction[0]
    if (output == 1):
        pred = "You are safe!!  This is a Legitimate Website."

    else:
        pred = "You are on the wrong site. Be cautious!"
    return render_template('index.html', prediction_text='{}'.format(pred), url=url)

# Takes the input parameters fetched from the URL by inputScript and returns the predictions


@ app.route('/predict_api', methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
