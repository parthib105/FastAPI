# for custom data validation, use Field

from __future__ import annotations

import pprint
from typing_extensions import Self
from typing import List, Dict, Optional, Annotated
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field

# nested model
class Address(BaseModel):
    street: str
    city: str
    PS: str
    district: str
    state: str
    pin: str
    emergency: Annotated[Optional[str], Field(default=None, max_length=10)]
                         
class Patient(BaseModel):
    name: str = Field(max_length=50)
    age: int
    email: EmailStr
    linkedin_url: AnyUrl
    weight: Annotated[float, Field(gt=0, strict=True)]     # weight can't be negative
    height: Annotated[float, Field(strict=True)]
    married: Annotated[bool, Field(default=False, description="Is the patient married or not")]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Address

    @field_validator('email')
    @classmethod
    def email_validator(cls, val: EmailStr) -> EmailStr:
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = val.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return val


    @field_validator('name')
    @classmethod
    def transform_username(cls, val: str) -> str:
        return val.upper()


    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, val: int) -> int:
        if 0 < val <= 100:
            return val
        else:
            raise ValueError("Age should be in between 0 and 100")


    # to check if the patient have emergency contact number
    @model_validator(mode='after')
    def validate_emergency_contact(self) -> Self:
        if self.age > 60:
            emergency_val = self.contact_details.emergency
            if not emergency_val or not emergency_val.strip():
                raise ValueError("Patient older than 60 must have an emergency contact number")

        return self


    @computed_field
    @property
    def bmi(self: Self) -> float:
        _bmi: float = round(self.weight / (self.height**2), 3)
        return _bmi


def insert_patient_data(p: Patient):
    print(p)
    print("Inserted into the database")


def update_patient_data(p: Patient):
    print(p.name)
    print(p.age)
    print(p.allergies)
    print(f"bmi = {p.bmi}")
    print("Updated into the database")



if __name__ == '__main__':
    addr_dict: Dict[str, str] = {
            "street": "Kumarsanda",
            "city": "Kumarsanda",
            "PS": "Kandi",
            "district": "Murshidabad",
            "state": "West Bengal", 
            "pin": "742136",
            "emergency": "6294112460"
        }

    add1: Address = Address(**addr_dict)
    
    p1_info = {
        "name": "Parthib", 
        "age": 83,
        "email": "parthibg105@hdfc.com",
        "linkedin_url": "https://www.linkedin.com/parthib-ghosh",
        "weight": 68.75,
        "height": 1.63,
        "married": False,
        "allergies": ['pollen', 'dust'],
        "contact_details": add1
    }

    pat1 = Patient(**p1_info)
    # insert_patient_data(pat1)

    update_patient_data(pat1)

    print()

    temp = pat1.model_dump()
    pprint.pp(temp)
