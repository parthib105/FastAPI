import pandas as pd
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .model.predict import my_model, MODEL_VERSION, predict_output
from .schema.user_input import UserInput
from .schema.prediction_response import PredictionResponse


router = APIRouter()

@router.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': my_model is not None
    }


@router.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):
    input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        pred = predict_output(input)
        return JSONResponse(status_code=200, content={'response': pred})
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))