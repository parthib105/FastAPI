import json
from pathlib import Path
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter()

CURR_DIR = Path(__file__).resolve().parent.parent
DATA_FILE_PATH = CURR_DIR / "patients.json" 

def load_data() -> Dict[str, Any]:
    with open(DATA_FILE_PATH, "r") as f:
        data = json.load(f)
    
    return data


def save_data(data) -> None:
    with open(DATA_FILE_PATH, "w") as f:
        json.dump(data, f)


@router.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}

@router.get("/view")
def view():
    return load_data()