Document Management System Backend:

Setup:
1.Install Python 3.9+
2.Create a virtual environment and activate it
3.Install dependencies: pip install -r requirements.txt
4.Set up PostgreSQL database:
 4.1:Create database: CREATE DATABASE db_name;
 4.2:Set DATABASE_URL environment variable, e.g., export DATABASE_URL=postgresql://user:password@localhost/db_name
5.Set SECRET_KEY environment variable for JWT, e.g., export SECRET_KEY=your-secret-key
6.Run the application: uvicorn main:app --host 0.0.0.0 --port 8000

Features:

User authentication with JWT
Role-based access control (admin, editor, viewer)
Document management (upload, list)
Ingestion management (trigger, list)

Testing:

Run tests with pytest tests/





Final Checks:

Make sure the .env file is at the project root.

Make sure PostgreSQL on your AWS EC2:

Is accepting external connections

Has port 5432 open in the security group

Has listen_addresses = '*' in postgresql.conf

Has host all all 0.0.0.0/0 md5 in pg_hba.conf (for test/dev access)

To Run:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"# Document_Management_Backend" 
