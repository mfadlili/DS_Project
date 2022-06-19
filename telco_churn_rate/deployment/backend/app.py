from flask import Flask, jsonify, request
import pickle
import pandas as pd
from tensorflow.keras.models import load_model

app = Flask(__name__)

LABEL = ['Not Churn', 'Churn']
columns = ['SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'MultipleLines',
       'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
       'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
       'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges']

with open("prep_pipe.pkl", "rb") as f:
    prep_pipe = pickle.load(f)

model = load_model("model_best.hdf5")

@app.route("/")
def homepage():
    return "<h1>Backend Pemodelan Milestone 1 Phase 2</h1>"

@app.route("/churn", methods=["GET", "POST"])
def potability_inference():
    if request.method == 'POST':
        data = request.json
        new_data = [data['SeniorCitizen'], 
                    data['Partner'], 
                    data['Dependents'], 
                    data['tenure'],
                    data['MultipleLines'],
                    data['InternetService'],
                    data['OnlineSecurity'],
                    data['OnlineBackup'],
                    data['DeviceProtection'],
                    data['TechSupport'],
                    data['StreamingTV'],
                    data['StreamingMovies'],
                    data['Contract'],
                    data['PaperlessBilling'],
                    data['PaymentMethod'],
                    data['MonthlyCharges']]

        new_data = pd.DataFrame([new_data], columns=columns)
        preprocessing = prep_pipe.transform(new_data)
        res = model.predict(preprocessing)
        response = {'code':200, 'status':'OK', 
                    'result':float(res[0][0])}
        return jsonify(response)
    
    return "Silahkan gunakan method POST"

