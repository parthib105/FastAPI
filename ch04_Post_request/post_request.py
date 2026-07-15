
import json
from typing import Annotated, Literal
from fastapi.responses import JSONResponse
from fastapi import HTTPException, APIRouter
from ch01_HTTP_methods import load_data, save_data
from pydantic import BaseModel, Field, computed_field


class Patient(BaseModel):

    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001', 'P003'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient lives")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in mtrs")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 3)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Need work out"
        else:
            return "Obese"


router = APIRouter()

@router.post("/create")
def create_patient(patient: Patient) -> JSONResponse:

    # load existing data
    curr_data = load_data()

    # check if the patient already exists
    if patient.id in curr_data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # add new patient
    curr_data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(curr_data)

    return JSONResponse(status_code=201, content={'message': 'patient created successfully'})