from fastapi import FastAPI
from routes import employee
from routes import leave

app = FastAPI()

app.include_router(employee.router, prefix="/api", tags=["Dashboard"])

app.include_router(leave.router, prefix="/api", tags=["Leave"])

@app.get("/")
def root():
    return {"message": "Leave Planner API is running"}
