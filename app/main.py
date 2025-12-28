from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud, database
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Project Management API')

# Dependency

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Projects
@app.post('/projects', response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project)

@app.get('/projects', response_model=List[schemas.Project])
def list_projects(skip: int = 0, limit: int = 50, sort_by: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return crud.get_projects(db, skip=skip, limit=limit, sort_by=sort_by)

# Workers
@app.post('/workers', response_model=schemas.Worker)
def create_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    return crud.create_worker(db, worker)

@app.get('/workers', response_model=List[schemas.Worker])
def list_workers(skip: int =0, limit: int=50, sort_by: Optional[str]=Query(None), db: Session = Depends(get_db)):
    return crud.get_workers(db, skip=skip, limit=limit, sort_by=sort_by)

# Assignments
@app.post('/assignments', response_model=schemas.Assignment)
def create_assignment(a: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    return crud.create_assignment(db, a)

@app.get('/assignments', response_model=List[schemas.Assignment])
def list_assignments(skip: int =0, limit: int=50, sort_by: Optional[str]=Query(None), db: Session = Depends(get_db)):
    return crud.get_assignments(db, skip=skip, limit=limit, sort_by=sort_by)

@app.get('/assignments/search')
def assignments_search(project_name: Optional[str]=None, worker_fio: Optional[str]=None, db: Session = Depends(get_db)):
    return crud.search_assignments_where(db, project_name, worker_fio)

@app.get('/assignments/joined')
def assignments_joined(db: Session = Depends(get_db)):
    return crud.assignments_joined(db)

@app.post('/assignments/update_real_end')
def update_real_end(cutoff_date: str, db: Session = Depends(get_db)):
    ids = crud.update_assignments_nontrivial(db, cutoff_date)
    return {"updated_ids": ids}

@app.get('/reports/workload_by_worker')
def report_workload(db: Session = Depends(get_db)):
    return crud.workload_group_by_worker(db)

@app.get('/assignments/regex_search')
def regex_search(q: str, db: Session = Depends(get_db)):
    return crud.regex_search_on_json(db, q)
