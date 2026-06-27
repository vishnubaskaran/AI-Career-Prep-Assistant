from pydantic import BaseModel


class UserInput(BaseModel):
    company: str
    skills: list[str]


class ProgressInput(BaseModel):
    company: str
    skill: str
    completed: bool