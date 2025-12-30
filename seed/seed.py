import requests
from random import randint, choice
from datetime import date, timedelta

BASE = 'http://localhost:8000'

def create_projects(n=20):
    for i in range(n):
        payload = {
            'shifr': f'PRJ-{i}',
            'name': f'Project {i}',
            'workload': randint(10,200)
        }
        requests.post(BASE + '/projects', json=payload)

def create_workers(n=20):
    positions = ['Engineer','Manager','Analyst','Tester']
    for i in range(n):
        payload = {'fio': f'Worker {i}', 'position': choice(positions)}
        requests.post(BASE + '/workers', json=payload)

def create_assignments(n=200):
    for i in range(n):
        payload = {
            'project_id': randint(1,20),
            'worker_id': randint(1,20),
            'workload': randint(1,40),
            'data': {'notes': f'auto generated assignment {i}', 'tags': ['auto','seed', f't{i%5}']}
        }
        requests.post(BASE + '/assignments', json=payload)

if __name__ == '__main__':
    create_projects()
    create_workers()
    create_assignments()
    print('Seeding done')
