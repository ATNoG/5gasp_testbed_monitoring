# generic imports
from typing import List
from pydantic import BaseModel
import datetime

class Targets(BaseModel):
    auth_token: str
    targets: list