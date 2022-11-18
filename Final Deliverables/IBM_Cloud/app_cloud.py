import requests
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
# importing the inputScript file used to analyze the URL
import InputScript
from fjagepy import Gateway


# load model
app = Flask(__name__, template_folder='template')

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "ouvZV8XvE5LPbgMrp55ollbnqU6K5e5RwnUsPKFsLrRU"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + mltoken}

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
    # checkprediction = InputScript.main(url)
    # print(checkprediction)
    # prediction = model.predict(checkprediction)
    # print(prediction)
    # output1 = prediction[0]
    # checkprediction = InputScript.main(url)
    # print(checkprediction)
    payload_scoring = {"input_data": [
        {"fields": url, "values": InputScript.main(url)}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/afc51492-4011-4a9e-b1b0-f0a2df1c8476/predictions?version=2022-11-15', json=payload_scoring,
                                     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    pred = response_scoring.json()
    print(pred)
    output = pred['predictions'][0]['values'][0][0]
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
