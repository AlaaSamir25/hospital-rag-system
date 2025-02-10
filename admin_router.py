from fastapi import APIRouter, HTTPException
from database import tables, fetch_all_records, create_record, update_record, delete_record
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

class RecordCreate(BaseModel):
    data: dict

class RecordUpdate(BaseModel):
    data: dict

@router.get("/tables")
def get_available_tables():
    return {"tables": list(tables.keys())}

@router.get("/{table}")
def read_table(table: str):
    if table not in tables:
        raise HTTPException(status_code=404, detail="Table not found")
    return fetch_all_records(table, tables[table])

@router.post("/{table}")
def create_table_record(table: str, record: RecordCreate):
    if table not in tables:
        raise HTTPException(status_code=404, detail="Table not found")
    return create_record(table, record.data)

@router.put("/{table}/{record_id}")
def update_table_record(table: str, record_id: int, record: RecordUpdate):
    if table not in tables:
        raise HTTPException(status_code=404, detail="Table not found")
    return update_record(table, record_id, record.data)

@router.delete("/{table}/{record_id}")
def delete_table_record(table: str, record_id: int):
    if table not in tables:
        raise HTTPException(status_code=404, detail="Table not found")
    return delete_record(table, record_id)