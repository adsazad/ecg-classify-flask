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
import pandas as pd
import keras

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

@app.route("/rrglu", methods=['POST'])
def rrglu():
    user = checkAuth(request)
    if user != True:
      return jsonify({"error": "Invalid auth token"})
    # make empty datatable
    age = request.json["age"]
    gender = request.json["gender"]
    ht = request.json["ht"]
    wt = request.json["wt"]
    rr = request.json["rr"]
    # explode rr with comma
    rr = rr.split(',')

    d = {'age': [age], 'gender': [gender], 'ht': [ht], 'wt': [wt]}
    for i in range(300):
      k = f'rr{i}'
      d[k] = [int(rr[i])]
    data = pd.DataFrame(data=d)
    # print(data)
    print(data.dtypes)
    # # data = pd.DataFrame()
    # # # add fields age, gender, ht,wt, and rr from rr0 to rr299
  
    model = keras.models.load_model('rrmodel.h5')
    # # # # predict
    # # print(data)
    # # xpred = np.asarray(data).astype(np.float32)
    # # print(xpred)

    prediction = model.predict(data)
    print(prediction)
    return jsonify({"glu": str(prediction[0])})


    return jsonify({"message": "Hello, World!"})
    

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
    # limit numpy array to 9000 entries
    numpy_array = numpy_array[:9000]
    # convert to np array
    numpy_array = np.array(numpy_array)
    scaler = pickle.load(open('scaler.sav', 'rb'))
    ecg = scaler.transform([numpy_array])
    ecg = np.reshape(ecg, (ecg.shape[0], 1, ecg.shape[1]))  # Reshape the numpy array
    model = keras.models.load_model('model.h5')
    prediction = model.predict(ecg)
    prediction = np.argmax(prediction, axis=1)
    label_mapping = {0:'A', 1:"N", 2:"O", 3:"~"}
    prediction = label_mapping[prediction[0]]
    return jsonify({"ecg": prediction})
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True,port=5003)

   

    


