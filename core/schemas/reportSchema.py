from pydantic import BaseModel

class reportProblem(BaseModel):
    title: str
    description: str