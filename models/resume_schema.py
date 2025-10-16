from pydantic import BaseModel
from typing import List

class Resume(BaseModel):
    name: str
    email: str
    skills: List[str]
    experience: List[str]
    education: List[str]
