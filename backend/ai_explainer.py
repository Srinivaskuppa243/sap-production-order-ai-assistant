def build_ai_prompt(diagnosis):
    if "error" in diagnosis:
        return diagnosis["error"]

    issues = diagnosis.get("issues", [])

    prompt = f"""
You are an SAP production planning assistant.

Analyze the following production order diagnosis.

Production Order: {diagnosis['order_id']}
Material: {diagnosis['material']}
Plant: {diagnosis['plant']}
Order Quantity: {diagnosis['order_quantity']}
Status: {diagnosis['status']}

Issues:
"""

    for issue in issues:
        prompt += f"""
Issue: {issue.get('issue', 'Unknown issue')}
Severity: {issue.get('severity', 'UNKNOWN')}
Evidence: {issue.get('evidence', 'No evidence available.')}
Recommendation: {issue.get('recommendation', 'No recommendation available.')}
"""

    prompt += """
Provide:
1. A concise explanation of the main production problem.
2. The highest-priority issue.
3. Why that issue matters.
4. Recommended next action.

Use only the evidence provided. Do not invent SAP data.
"""

    return prompt
if __name__ == "__main__":
    from backend.diagnostic_engine import diagnose_production_order

    order_id = input("Enter production order ID: ")
    diagnosis = diagnose_production_order(order_id)

    prompt = build_ai_prompt(diagnosis)

    print("\n--- AI PROMPT ---\n")
    print(prompt)