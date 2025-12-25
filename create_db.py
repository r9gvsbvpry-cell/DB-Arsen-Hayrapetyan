import os
import psycopg2

PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = int(os.getenv('PG_PORT', '5432'))
PG_SUPERUSER = os.getenv('PG_SUPERUSER', 'postgres')
PG_SUPERPASS = os.getenv('PG_SUPERPASS', '')
DB_NAME = os.getenv('DB_NAME', 'pm_db')
DB_OWNER = os.getenv('DB_OWNER', 'pm_user')
DB_OWNER_PASS = os.getenv('DB_OWNER_PASS', 'pm_pass')

conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, user=PG_SUPERUSER, password=PG_SUPERPASS)
conn.autocommit = True
cur = conn.cursor()

try:
    cur.execute(f"CREATE ROLE {DB_OWNER} WITH LOGIN PASSWORD %s;", (DB_OWNER_PASS,))
except Exception:
    print('Role may already exist, continuing')

try:
    cur.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_OWNER};")
except Exception:
    print('Database may already exist, continuing')

cur.close()
conn.close()
print('create_db.py finished')
