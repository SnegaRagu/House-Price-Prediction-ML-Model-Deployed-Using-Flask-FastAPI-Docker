from fastapi import FastAPI
from fastapi import HTTPException
import numpy as np
from app.model import predict_price
from app.schemas import HouseFeatures
from app.utils import make_dataframe

app = FastAPI(
    title = "🏠 House Price Prediction API",
    description = "Predict Bengaluru house prices using different ML models",
    version = "1.0.0"
)

@app.get("/")
def root():
    return {
        "message" : "Welcome to House Price Prediction API (FastAPI) !",
        "tools" : ["Python", "Scikit-learn", "Pandas", "Numpy", "Joblib", "ML Models", "FastAPI", "JSON"]
    }

@app.get("/info")
def info():
    return {
        "model_name"        : ["XGBoost", "Random Forest", "Linear Regression", "Random Forest"],
        "version"           : "1.0.0",
        "methods"           : ["GET", "POST"],
        "expected_features" : ["area_type", "availability", "location", "size", "total_sqft", "bath", "balcony"]
    }

@app.post("/predict")
def predict(features: HouseFeatures):
    try:
        df = make_dataframe(features)
        print("\n=== Preprocessing started ===")

        # your model's pipeline (preprocessor + model)
        res = predict_price(df, features.model_name)

        # Convert numpy or pandas types to Python native
        if isinstance(res, (np.generic, np.ndarray)):
            res = np.array(res).item() if np.ndim(res) == 0 else float(res[0])

        # Convert df to a JSON-friendly format
        input_data_dict = df.to_dict(orient="records")[0]

        return {
            "Model name": features.model_name,
            "Input data": input_data_dict,
            "Predicted Price (Lakh ₹)": round(res, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
