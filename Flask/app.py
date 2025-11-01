from flask import Flask, request, jsonify, Response
import json
import joblib
import pandas as pd

from custom_function import simplify_availability, convert_bhk, conv_sqft

# Create Flask App
app = Flask(__name__)

# Load Models

with open("models/linear_regression.pkl", "rb") as f:
    lr_model = joblib.load(f)
with open("models/polynomial_regression.pkl", "rb") as f:
    poly_model = joblib.load(f)
with open("models/RandomForest.pkl", "rb") as f:
    rf_model = joblib.load(f)
with open("models/XGBoost.pkl", "rb") as f:
    xgb_model = joblib.load(f)


# Default Route
@app.route('/')
def home():
    info = {"message" : "Welcome to House Price Prediction API!",
            "tools"   : ["Python", "Sklearn", "Flask", "JSON", "Numpy", "Pandas", "Joblib"],
            "routes"  : ["/info", "/predict"],
            "methods" : ["GET", "POST"]}

    json_str = json.dumps(info, indent=4)
    return Response(json_str, mimetype='application/json')

# Info Route
@app.route('/info', methods=["GET"])
def info():
    print("\nInfo fetched with GET")
    info = {
        "project": "House Price Prediction API",
        "version": "1.0.0",
        "description": "Predict house prices using different ML models.",
        "models" : [{
            "model_name"        : "XGBoost Regression Model - xgb",
            "file"              : "models/XGBoost.pkl",
            "version"           : "1.0",
            "methods"           : ["GET", "POST"],
            "expected_features" : ["area_type", "availability", "location", "size", "total_sqft", "bath", "balcony"]
        },{
            "model_name"        : "Random Forest Regression Model - rf",
            "file"              : "models/RandomForest.pkl",
            "version"           : "1.0",
            "methods"           : ["GET", "POST"],
            "expected_features" : ["area_type", "availability", "location", "size", "total_sqft", "bath", "balcony"]
        },{
            "model_name"        : "Linear Reagression Model - lr",
            "file"              : "models/linear_regression.pkl",
            "version"           : "1.0",
            "methods"           : ["GET", "POST"],
            "expected_features" : ["area_type", "availability", "location", "size", "total_sqft", "bath", "balcony"]
        },{
            "model_name"        : "Polynomial Regression Model - poly",
            "file"              : "models/polynomial_regression.pkl",
            "version"           : "1.0",
            "methods"           : ["GET", "POST"],
            "expected_features" : ["area_type", "availability", "location", "size", "total_sqft", "bath", "balcony"]
    }]}
    json_str = json.dumps(info, indent=4)
    return Response(json_str, mimetype='application/json')

# Predict Route
@app.route('/predict', methods=["POST"])
def predict():
    try:
        print("\nPredict created with POST")
        '''
        { "data" : {"columns" : ["area_type", "availability", "location", "size", "total_sqft", "bath", "balcony", "model_name"],
            "values"  : [["Plot area", "10", "Devanahalli", "2 BHK","15000Grounds",2, 1,"xgb"]]}}
        '''
        data = request.get_json()

        # Extract dataframe
        columns = data['data']['columns']
        values = data['data']['values']
        df = pd.DataFrame(values, columns=columns)

        # Extract and remove model name
        model_name = df["model_name"].iloc[0]
        df = df.drop(columns=["model_name"])

        print("\n========== Incoming Data ==========")
        print(df)
        print(df.isna().sum())
        print("Model name:", model_name)

        if model_name == 'rf':
            print("\nUsing RF model...")
            pred = rf_model.predict(df)[0]

        elif model_name == 'xgb':
            print("\nUsing XGB model...")
            pred = xgb_model.predict(df)[0]

        elif model_name == 'lr':
            print("\nUsing LR model...")
            pred = lr_model.predict(df)[0]

        elif model_name == 'poly':
            print("\nUsing POLYNOMIAL model...")
            pred = poly_model.predict(df)[0]

        else:
            return jsonify({"error": "Invalid Model Name"}), 400

        print("\nPrediction DONE:", pred)

        return jsonify({
            "Model name": model_name,
            "Input data": data,
            "Predicted Price (Lakh ₹)": f"{pred:,.2f}"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
