from pydantic import BaseModel


class TasksGet(BaseModel):
    build: str
