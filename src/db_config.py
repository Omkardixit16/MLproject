# src/db_config.py
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            database="ml_project",
            user="root",
            password="Abcd1234#$"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None
