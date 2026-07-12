import json
from fastapi import APIRouter

router = APIRouter()

def load_data():
    with open("../patients.json", "r") as f:
        data = json.load(f)
    
    return data

@router.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}

@router.get("/view")
def view():
    return load_data()