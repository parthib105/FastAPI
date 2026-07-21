import pickle
import pandas as pd
from pathlib import Path
from fastapi import APIRouter
from typing import Literal, Annotated
from fastapi.responses import JSONResponse
from .model import tier_1_cities, tier_2_cities
from pydantic import BaseModel, Field, computed_field

# Load the serialized model. Use a path relative to this file so the
# import works regardless of the cwd from which uvicorn is launched.
model_path = Path(__file__).with_name('trained_model.pkl')
if not model_path.is_file():
    raise FileNotFoundError(
        f"Trained model not found at {model_path!s}. "
        "Run `python -m ch06_MLmodels_and_fastapi.model` to generate it."
    )
with open(model_path, 'rb') as f:
    my_model = pickle.load(f)

router = APIRouter()

# pydantic model
class UserInput(BaseModel):
    
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the user')]
    income_lpa: Annotated[float, Field(..., gt=0, description='Annual salary of the user in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker')]
    city: Annotated[str, Field(..., description='The city that the user belongs to')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker and self.bmi > 27:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3


@router.post('/predict')
def predict_premium(data: UserInput):
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction = my_model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'predicted_category': prediction})