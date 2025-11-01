import pandas as pd
import numpy as np
import re

# Converting ready to move as 1 since others are planned

def simplify_availability(val):
    print("\nsimplify_availability called with:\n", val)
    '''
    if isinstance(val, pd.Series):
        return val.apply(lambda val: 1 if isinstance(val, str) and ("Ready" in val.lower() or "Immediate" in val.lower()) else 0)
    elif isinstance(val, str):
        return 1 if ("Ready" in val.lower() or "Immediate" in val.lower()) else 0
    else:
        return 0

    '''
    val = pd.Series(np.ravel(val))
    converted = val.apply(lambda val : 1 if isinstance(val, str) and ("Ready" in val.lower() or "Immediate" in val.lower()) else 0)
    return converted.values.reshape(-1, 1)
    

# Converting Bedroom to BHK in size

def convert_bhk(val):
    print("\nconvert_bhk called with:\n", val)
    # Flatten to 1D array
    val = pd.Series(np.ravel(val))
    converted = val.apply(lambda val : val.replace("Bedroom", "BHK").replace("bedroom", "BHK") if isinstance(val, str) and "bedroom" in val.lower() else val)
    return converted.values.reshape(-1, 1)

# Total Square Feet Area --> ranges converted to average and float

def conv_sqft(val):
    print("\nconv_sqft called with:\n", val)

    # ✅ Handle both DataFrame and Series inputs
    if isinstance(val, pd.DataFrame):
        val = val.iloc[:, 0]  # take first column
    elif not isinstance(val, pd.Series):
        val = pd.Series(val)

    def conv_single(v):
        try:
            if isinstance(v, (int, float)):
                return float(v)
            elif isinstance(v, str):
                v = v.strip()

                # Range Case: e.g. "2100 - 2850"
                if " - " in v:
                    parts = v.split(" - ")
                    if len(parts) == 2:
                        return (float(parts[0]) + float(parts[1])) / 2

                # Normalize: add space between number and letters
                v = re.sub(r"(?<=\d)([A-Za-z])", r" \1", v)
                v_lower = v.lower()

                # Unit Case (case-insensitive)
                if re.search(r'[a-zA-Z]', v):
                    print("\nReached Unit case:", v)
                    num = re.findall(r'^[\d\.]+', v)
                    if not num:
                        return np.nan
                    n = float(num[0])

                    if "sq. meter" in v_lower or "square meter" in v_lower:
                        return round(n * 10.7639, 2)
                    elif "perch" in v_lower:
                        return round(n * 272.25, 2)
                    elif "sq. yard" in v_lower or "square yard" in v_lower:
                        return round(n * 9, 2)
                    elif "acre" in v_lower:
                        return round(n * 43560, 2)
                    elif "cent" in v_lower:
                        return round(n * 435.6, 2)
                    elif "ground" in v_lower:
                        return round(n * 2400, 2)
                    elif "guntha" in v_lower:
                        return round(n * 1089, 2)

                # Plain numeric case
                return float(v)
        except Exception as e:
            print("Error converting:", v, e)
            return np.nan

    converted = val.apply(conv_single)
    print("\nConversion SQFT done:\n", converted)
    return converted.values.reshape(-1, 1)


# Converting Input JSON Data to DataFrame

def make_dataframe(input_data):
    d = dict(input_data)
    return pd.DataFrame([{
        "area_type" : d['area_type'],
        "availability" : d['availability'],
        "location": d['location'],
        "size": d['size'],
        "total_sqft": d['total_sqft'],
        "bath": d['bath'],
        "balcony": d['balcony']
    }])