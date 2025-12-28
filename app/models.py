from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    shifr = Column(String(64), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    deadline = Column(Date)
    workload = Column(Integer)

    assignments = relationship('Assignment', back_populates='project')

class Worker(Base):
    __tablename__ = 'workers'
    id = Column(Integer, primary_key=True)
    fio = Column(String(200), nullable=False)
    position = Column(String(100))

    assignments = relationship('Assignment', back_populates='worker')

class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    issue_date = Column(Date)
    planned_end = Column(Date)
    real_end = Column(Date)
    workload = Column(Integer)
    data = Column(JSONB, default={})

    project = relationship('Project', back_populates='assignments')
    worker = relationship('Worker', back_populates='assignments')
