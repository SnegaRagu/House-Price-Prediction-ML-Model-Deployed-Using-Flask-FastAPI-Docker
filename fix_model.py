"""
This script safely reloads existing model pipelines and re-saves them
with correct references to custom functions in app.utils.

Run it once before deploying your FastAPI app.
"""

import joblib
from pathlib import Path
from app.utils import simplify_availability, convert_bhk, conv_sqft

# --- Register functions globally so joblib can find them ---
globals()["simplify_availability"] = simplify_availability
globals()["convert_bhk"] = convert_bhk
globals()["conv_sqft"] = conv_sqft

# --- Correct model directory (outside app/) ---
MODEL_DIR = Path("models")

# --- Detect all pickle files automatically ---
model_files = list(MODEL_DIR.glob("*.pkl"))

if not model_files:
    print("⚠️ No .pkl files found in 'model/' directory.")
else:
    for model_path in model_files:
        print(f"Fixing {model_path.name} ...")
        try:
            model = joblib.load(model_path)
            joblib.dump(model, model_path)
            print(f"✅ Re-saved: {model_path}")
        except Exception as e:
            print(f"❌ Error fixing {model_path.name}: {e}")

    print("\n✅ All models re-saved with correct function references.")