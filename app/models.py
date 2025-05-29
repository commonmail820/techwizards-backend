from pydantic import BaseModel

class SignupData(BaseModel):
    name: str
    email: str
    password: str