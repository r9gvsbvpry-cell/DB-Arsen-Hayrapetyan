from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import date

class ProjectBase(BaseModel):
    shifr: str
    name: str
    deadline: Optional[date]
    workload: Optional[int]

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    class Config:
        orm_mode = True

class WorkerBase(BaseModel):
    fio: str
    position: Optional[str]

class WorkerCreate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int
    class Config:
        orm_mode = True

class AssignmentBase(BaseModel):
    project_id: int
    worker_id: int
    issue_date: Optional[date]
    planned_end: Optional[date]
    real_end: Optional[date]
    workload: Optional[int]
    data: Optional[Any]

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    id: int
    class Config:
        orm_mode = True
