from flask import Flask,jsonify,request 
from auth.checkauth import checkAuth
import os
import json
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Conv1D
from keras.layers import MaxPooling1D
from keras.layers import BatchNormalization
from keras.layers import Activation
from keras.layers import GlobalAveragePooling1D


app = Flask(__name__)
app.debug = True


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "No Route Exist"}), 404

# Define a route that triggers a 404 error
# @app.route('/404', methods=['GET'])
# def not_found_route():
#     # Simulate a situation where the route does not exist
#     return 'This route does not exist!', 404

@app.route("/classify/ecg", methods=['POST'])
def predict_api():
     # check authentication
    
    user = checkAuth(request)
    if user != True:
      return jsonify({"error": "Invalid auth token"})
    
    # print(request.json)
    ecg = request.form.get('ecg')
    if not ecg:
      return jsonify({"error": "Missing 'ecg' parameter"})
    # jsondecode ecg
    ecg = json.loads(ecg)
    numpy_array = np.array([float(value) for value in ecg])
    scaler = pickle.load(open('scaler.sav', 'rb'))
    numpy_array = scaler.transform([numpy_array])
    ecg = np.reshape(ecg, (ecg.shape[0], 1, ecg.shape[1]))
    model = pickle.load(open('model.m5', 'rb'))
    prediction = model.predict(ecg)
    prediction = np.argmax(prediction, axis=1)
    label_mapping = {0:'A', 1:"N", 2:"O", 3:"~"}
    prediction = label_mapping[prediction[0]]
    return jsonify({"ecg": prediction})
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=5003)

   

    


