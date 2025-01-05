import logging
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
            print(db_path)
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
