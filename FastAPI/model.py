import joblib
from fastapi import HTTPException


from app import utils

globals()['simplify_availability'] = utils.simplify_availability
globals()['convert_bhk'] = utils.convert_bhk
globals()['conv_sqft'] = utils.conv_sqft

with open("models/RandomForest.pkl", "rb") as f:
    rf_model = joblib.load(f)
with open("models/XGBoost.pkl", "rb") as f:
    xgb_model = joblib.load(f)
with open("models/linear_regression.pkl", "rb") as f:
    lr_model = joblib.load(f)
with open("models/polynomial_regression.pkl", "rb") as f:
    poly_model = joblib.load(f)

def predict_price(data, model_name="xgb"):
    if model_name == "rf":
        model = rf_model
    elif model_name == "lr":
        model = lr_model
    elif model_name == "poly":
        model = poly_model
    elif model_name == "xgb":
        model = xgb_model
    else:
        raise HTTPException(status_code=400, detail=f"Model '{model_name}' not found")

    pred = model.predict(data)
    return round(float(pred[0]), 2)