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

    def add_product(self, name):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO products (name) VALUES (?)", (name,))
        self.conn.commit()

    def get_product_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, quantity FROM products WHERE name = ?", (name,))
        return cursor.fetchone()

    def update_product_quantity(self, product_id, quantity):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (quantity, product_id))
        self.conn.commit()

    def add_receipt(self, product_id, date, quantity):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO receipts (product_id, date, quantity) VALUES (?, ?, ?)",
                       (product_id, date, quantity))
        self.conn.commit()

    def add_issue(self, product_id, date, quantity):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO issues (product_id, date, quantity) VALUES (?, ?, ?)",
                       (product_id, date, quantity))
        self.conn.commit()

    def get_all_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, quantity FROM products")
        return cursor.fetchall()

    def get_product_by_id(self, product_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, quantity FROM products WHERE id = ?", (product_id,))
        return cursor.fetchone()

    def search_products_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, quantity FROM products WHERE name LIKE ?", ('%' + name + '%',))
        return cursor.fetchall()

    def update_product(self, product_id, name, quantity):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE products SET name = ?, quantity = ? WHERE id = ?", (name, quantity, product_id))
        self.conn.commit()

    def restore_database(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute("DROP TABLE IF EXISTS receipts")
        cursor.execute("DROP TABLE IF EXISTS issues")
        self.create_tables()
