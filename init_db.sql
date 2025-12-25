-- Example SQL to create a database and owner. Run as a superuser in psql.
CREATE ROLE pm_user WITH LOGIN PASSWORD 'pm_pass';
CREATE DATABASE pm_db OWNER pm_user;
-- Grant privileges if needed
GRANT ALL PRIVILEGES ON DATABASE pm_db TO pm_user;
