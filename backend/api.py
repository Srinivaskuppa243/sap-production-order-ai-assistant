from fastapi import FastAPI
from backend.diagnostic_engine import diagnose_production_order
from backend.diagnostic_engine import summarize_diagnosis
from backend.ai_explainer import generate_explanation

app = FastAPI(title="SAP Production Order AI Assistant")


@app.get("/")
def home():
    return {"message": "SAP Production Order AI Assistant API is running"}

@app.get("/diagnose/{order_id}")
def diagnose(order_id: str):
    return diagnose_production_order(order_id)

@app.get("/diagnose/{order_id}/summary")
def diagnose_summary(order_id: str):
    result = diagnose_production_order(order_id)
    return {"summary": summarize_diagnosis(result)}

@app.get("/diagnose/{order_id}/explanation")
def diagnose_explanation(order_id: str):
    result = diagnose_production_order(order_id)
    explanation = generate_explanation(result)

    return {"explanation": explanation}