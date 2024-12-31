from sqlalchemy import create_engine

# Connect to the default database
engine = create_engine("postgresql://postgres_turtle:HkeARf3g0L8XxBqlO1c6@turtle-tracking-db.cfw8ai2auz34.eu-west-1.rds.amazonaws.com:5432/postgres")
conn = engine.connect()

# Create the new database
conn.execute("commit")  # Required for CREATE DATABASE
conn.execute("CREATE DATABASE turtle_tracking_db;")
conn.close()