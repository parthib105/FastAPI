'''
The 'Path()' function in FastAPI is used to provide metadata, validation rules and documentation hints for path parameters in our API endpoints.

Title
Description
Example
ge, gt, le, lt
Min_length
Max_length
regex


Query parameters are optional key-value pairs appended to the end of a URL used to pass additional data to the server in an HTTP request. They are typically employed for operations like filtering, sorting, searching and paging, without altering the endpoint path itself

eg: /patient?city=Delhi&sort_by=age
'''

import json
from ch01_HTTP_methods import load_data
from fastapi import Path, Query
from fastapi import HTTPException, APIRouter

router = APIRouter()

@router.get("/patient/{pid}")
def view_patient(
    pid: str = Path(
        ...,
        title="Patient ID",
        description="The unique identifier for the patient, typically starting with 'P' followed by 3 digits (e.g., P001)."
    )
):
    
    data = load_data()
    
    if pid in data:
        return data[pid]
    return HTTPException(status_code=404, detail="Patient not found")

@router.get("/order")
def order_patients(
    sort_by: str = Query(
        ...,
        description='Sort on the basis of height, weight or bmi'
    ),
    order: str = Query(
        'asc',
        description='sort in ascending or descending'
    )
):
    valid_fields = ["height", "weight", "bmi"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, details=f"Invalid field, select from {valid_fields}")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f"Invalid order, select between asc and desc")
    
    data = load_data()
    
    sort_order: bool = True if order=='desc' else False
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    
    return sorted_data