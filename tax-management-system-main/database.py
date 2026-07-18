import sqlite3
import os

DB_FILE = "tax_system.db"

def get_db_connection():
    """Establishes an active database session with row factory enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name like a dictionary
    return conn

def initialize_database():
    """Executes the core SQL blueprint to build relational tables if they don't exist."""
    connection = get_db_connection()
    cursor = connection.cursor()

    # Enable Foreign Key enforcement in SQLite explicitly
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Clients Master Table Creation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # 2. Tax Records Relational Table Creation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TaxRecords (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            financial_year TEXT NOT NULL,
            gross_income REAL NOT NULL,
            deductions REAL NOT NULL,
            tax_payable REAL NOT NULL,
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES Clients (client_id) ON DELETE CASCADE
        );
    ''')

    connection.commit()
    connection.close()
    print("👉 Relational Database Schema Initialized Successfully [tax_system.db]")

if __name__ == '__main__':
    initialize_database()