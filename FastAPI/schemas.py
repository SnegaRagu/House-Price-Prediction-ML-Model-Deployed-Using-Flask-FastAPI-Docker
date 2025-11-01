# Pydantic - for request validation
# Defining Input Schema

from pydantic import BaseModel
from typing import Union

class HouseFeatures(BaseModel):
    area_type: str
    availability: Union[str, int, float]
    location: str
    size: str
    total_sqft: Union[str, int, float]
    bath: int
    balcony: int
    model_name: str = "xgb"