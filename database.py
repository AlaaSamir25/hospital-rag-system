import pyodbc
import os
from typing import List, Dict
from typing import List, Dict, Any
import pyodbc

tables = {
    "Physicians": ["Degree", "Name", "Speciality"],
    "Policy": ["Address", "Landline", "Name", "Open_Date", "Policy_Description"],
    "Pricelist": ["Price__USD_", "Service_Name"],
    "Schedules": ["Doctor_Name", "Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"],
    "Specialities": ["Definition", "Speciality_Name"]
}

def get_db_connection():
    server = "DESKTOP-VDIOHUC"
    database = "HIS_database"
    return pyodbc.connect(
        f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
    )

def fetch_all_records(table_name: str, columns: List[str]) -> List[Dict]:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = f"SELECT {', '.join(columns)} FROM [{table_name}]"
            cursor.execute(query)
            rows = cursor.fetchall()
            col_names = [column[0] for column in cursor.description]
            return [dict(zip(col_names, row)) for row in rows]
    finally:
        conn.close()



# ... (keep existing connection and fetch_all_records functions)

def execute_query(query: str, params: tuple = ()):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            if cursor.description:  # For SELECT statements
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return {"message": "Operation successful"}
    except pyodbc.Error as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()

def create_record(table: str, data: dict):
    columns = ", ".join([f"[{k}]" for k in data.keys()])
    placeholders = ", ".join(["?"] * len(data))
    query = f"INSERT INTO [{table}] ({columns}) VALUES ({placeholders})"
    return execute_query(query, tuple(data.values()))

def update_record(table: str, record_id: int, data: dict):
    set_clause = ", ".join([f"[{k}] = ?" for k in data.keys()])
    query = f"UPDATE [{table}] SET {set_clause} WHERE ID = ?"
    return execute_query(query, tuple(data.values()) + (record_id,))

def delete_record(table: str, record_id: int):
    query = f"DELETE FROM [{table}] WHERE ID = ?"
    return execute_query(query, (record_id,))