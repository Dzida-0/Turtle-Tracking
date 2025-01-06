import logging
import os
import sqlite3
import pymysql


class DatabaseHandler:
    def __init__(self, db_uri, is_rds=False):
        self.db_uri = db_uri
        self.is_rds = is_rds
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish a database connection"""
        if self.is_rds:
            # Connect to RDS MySQL
            self.conn = pymysql.connect(
                host=self.db_uri['host'],
                user=self.db_uri['user'],
                password=self.db_uri['password'],
                database=self.db_uri['database']
            )
        else:
            # Connect to SQLite

            db_path = self.db_uri
            os.makedirs(db_path, exist_ok=True)
            db_path = os.path.join(db_path, "database.db")
            self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        """
        Executes a query on the database and commits changes.
        """
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error executing query: {e}")
            raise

    def fetch_one(self, query, params=None):
        """Fetch a single result from a query."""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def rollback(self):
        """Rollback any uncommitted transaction."""
        if self.conn:
            self.conn.rollback()

    def create_basic_user(self):
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS turtle (
                id TEXT PRIMARY KEY,
                name TEXT,
                last_position TEXT,
                is_active TEXT,
                turtle_sex TEXT,
                turtle_age TEXT,
                length REAL,
                length_type TEXT,
                width REAL,
                width_type TEXT,
                project_name TEXT,
                biography TEXT,
                description TEXT,
                photo TEXT,
                distance_from_last FLOAT,
                avg_speed_from_last FLOAT
                
            )
        """)
