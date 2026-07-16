import json
from ch04_Post_request import Patient
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from ch01_HTTP_methods import load_data, save_data
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional, Dict, Any

class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None, description="Name of the patient")]
    city: Annotated[Optional[str], Field(default=None, description="City where the patient lives")]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None, description="Gender of the patient")]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="Height of the patient in mtrs")]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description="Weight of the patient in kgs")]


router = APIRouter()


@router.put("/edit/{p_id}")
def update_patient(p_id: str, patient_update: PatientUpdate):
    # load the existing data
    curr_data: Dict[str, Any] = load_data()

    if p_id not in curr_data:
        return HTTPException(status_code=404, detail="Patient not found")

    curr_patient_info: Dict[str, Any] = curr_data[p_id]

    updated_patient_info: Dict[str, Any] = patient_update.model_dump(exclude_unset=True)

    for key, val in updated_patient_info.items():
        curr_patient_info[key] = val

    # now we need to update the computed fields
    # curr_patient_info -> pydantic object
    curr_patient_info['id'] = p_id
    patient_pydantic_obj = Patient(**curr_patient_info)

    # pydantic object -> dict
    curr_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    # add to data
    curr_data[p_id] = curr_patient_info

    save_data(curr_data)

    return JSONResponse(status_code=200, content={"message": "Patient updated"})


@router.delete("/delete/{p_id}")
def delete_patient(p_id: str):

    # load the data
    curr_data = load_data()

    if p_id not in curr_data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del curr_data[p_id]

    save_data(curr_data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted"})

