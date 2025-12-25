from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
from sqlalchemy import func, and_, text

# Projects

def create_project(db: Session, project: schemas.ProjectCreate):
    db_obj = models.Project(shifr=project.shifr, name=project.name, deadline=project.deadline, workload=project.workload)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_projects(db: Session, skip: int = 0, limit: int = 100, sort_by: Optional[str]=None):
    q = db.query(models.Project)
    if sort_by:
        q = q.order_by(text(sort_by))
    return q.offset(skip).limit(limit).all()

# Workers

def create_worker(db: Session, worker: schemas.WorkerCreate):
    db_obj = models.Worker(fio=worker.fio, position=worker.position)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_workers(db: Session, skip: int = 0, limit: int = 100, sort_by: Optional[str]=None):
    q = db.query(models.Worker)
    if sort_by:
        q = q.order_by(text(sort_by))
    return q.offset(skip).limit(limit).all()

# Assignments

def create_assignment(db: Session, a: schemas.AssignmentCreate):
    db_obj = models.Assignment(**a.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_assignments(db: Session, skip: int =0, limit: int=100, sort_by: Optional[str]=None):
    q = db.query(models.Assignment)
    if sort_by:
        q = q.order_by(text(sort_by))
    return q.offset(skip).limit(limit).all()

def search_assignments_where(db: Session, project_name: Optional[str]=None, worker_fio: Optional[str]=None):
    q = db.query(models.Assignment).join(models.Project).join(models.Worker)
    if project_name:
        q = q.filter(models.Project.name.ilike(f"%{project_name}%"))
    if worker_fio:
        q = q.filter(models.Worker.fio.ilike(f"%{worker_fio}%"))
    return q.all()

def assignments_joined(db: Session):
    return db.query(models.Assignment, models.Project, models.Worker).join(models.Project).join(models.Worker).all()

def update_assignments_nontrivial(db: Session, cutoff_date):
    # Example: set real_end = now where planned_end < cutoff_date and real_end is null
    sql = text("UPDATE assignments SET real_end = :cutoff WHERE real_end IS NULL AND planned_end < :cutoff RETURNING id;")
    res = db.execute(sql, {"cutoff": cutoff_date})
    db.commit()
    return [r[0] for r in res]

def workload_group_by_worker(db: Session):
    return db.query(models.Worker.fio, func.sum(models.Assignment.workload).label('total'))\
        .join(models.Assignment).group_by(models.Worker.fio).all()

def regex_search_on_json(db: Session, pattern: str):
    # Uses raw SQL to leverage Postgres regex; pattern should be a POSIX/pg regex
    sql = text("SELECT * FROM assignments WHERE (data::text) ~ :pattern")
    res = db.execute(sql, {"pattern": pattern}).fetchall()
    return res
