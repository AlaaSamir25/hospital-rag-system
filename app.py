from fastapi import FastAPI
from pydantic import BaseModel
from query_processor import process_query
from admin_router import router as admin_router

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

# Include admin routes
app.include_router(admin_router)

@app.post("/ask")
async def handle_query(request: QueryRequest):
    response = process_query(request.query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)