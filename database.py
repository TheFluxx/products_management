import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        self.create_tables()

    def create_connection(self, db_file):
        """Создание подключения к базе данных SQLite"""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity REAL DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                date TEXT,
                quantity REAL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                date TEXT,
                quantity REAL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        self.conn.commit()


