from fastapi import FastAPI
from backend.diagnostic_engine import diagnose_production_order

app = FastAPI(title="SAP Production Order AI Assistant")


@app.get("/")
def home():
    return {"message": "SAP Production Order AI Assistant API is running"}


@app.get("/diagnose/{order_id}")
def diagnose(order_id: str):
    return diagnose_production_order(order_id)