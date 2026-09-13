import csv
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def load_csv(filename):
    file_path = DATA_DIR / filename

    with open(file_path, newline="") as file:
        return list(csv.DictReader(file))


def diagnose_production_order(order_id):
    orders = load_csv("production_orders.csv")
    inventory = load_csv("inventory.csv")
    bom = load_csv("bom.csv")
    routing=load_csv("routing.csv")
    confirmations = load_csv("confirmations.csv")
    order = next(
        (order for order in orders if order["order_id"] == order_id),
        None
    )

    if not order:
        return {"error": f"Production order {order_id} not found"}

    material = order["material"]
    plant = order["plant"]
    order_quantity = int(order["order_quantity"])

    material_bom = [
        item for item in bom
        if item["material"] == material
    ]
    
    material_routing=[
        item for item in routing
        if item["material"]== material
    ]
    issues = []

    if not material_bom:
        issues.append({
            "issue":"Missing BOM",
            "material":material
        })
    if not material_routing:
        issues.append({
            "issue":"Missing Routing",
            "material":material,
            "severity":"HIGH",
            "recommendation":"Check the production routing and maintain the required operations for this material."
            
        })
     # Check for unconfirmed operations
    order_confirmations = [
        row for row in confirmations
        if row["order_id"] == order_id
    ]

    for confirmation in order_confirmations:
        if confirmation["status"] == "NOT_CONFIRMED":
            issues.append({
                "order_id": order_id,
                "operation": confirmation["operation"],
                "issue": "Operation not confirmed",
                "severity": "MEDIUM",
                "recommendation": "Check the production order operation and confirm the operation if production has been completed."
            })
    for component in material_bom:
        component_material = component["component"]
        quantity_per_unit = float(component["quantity_per_unit"])

        required_quantity = order_quantity * quantity_per_unit

        stock_record = next(
            (
                item for item in inventory
                if item["material"] == component_material
                and item["plant"] == plant
            ),
            None
        )

        if not stock_record:
            issues.append({
                "component": component_material,
                "issue": "No inventory record found",
                "required": required_quantity,
                "available": 0,
                "shortage": required_quantity,
                "severity": "HIGH",
                "recommendation": "Check procurement or planning for the missing component quantity."
            })
            continue

        available_quantity = float(stock_record["unrestricted_stock"])
        shortage = max(required_quantity - available_quantity, 0)

        if shortage > 0:
            issues.append({
                "component": component_material,
                "issue": "Insufficient stock",
                "required": required_quantity,
                "available": available_quantity,
                "shortage": shortage,
                "severity": "HIGH",
                "recommendation": "Check procurement or planning for the missing component quantity."
            })

    return {
        "order_id": order_id,
        "material": material,
        "plant": plant,
        "order_quantity": order_quantity,
        "status": order["status"],
        "issues": issues
    }
    
def summarize_diagnosis(result):
    if "error" in result:
        return result["error"]

    lines = [
        f"Production Order: {result['order_id']}",
        f"Material: {result['material']}",
        f"Plant: {result['plant']}",
        f"Status: {result['status']}",
        "",
        "Issues Found:"
    ]

    if not result["issues"]:
        lines.append("No issues found.")
        return "\n".join(lines)

    for issue in result["issues"]:
        severity = issue.get("severity", "UNKNOWN")
        issue_name = issue.get("issue", "Unknown issue")
        recommendation = issue.get("recommendation", "No recommendation available.")

        lines.append(f"- [{severity}] {issue_name}")

        if "component" in issue:
            lines.append(
                f"  Component: {issue['component']} | "
                f"Required: {issue['required']} | "
                f"Available: {issue['available']} | "
                f"Shortage: {issue['shortage']}"
            )

        if "operation" in issue:
            lines.append(f"  Operation: {issue['operation']}")

        lines.append(f"  Recommendation: {recommendation}")

    return "\n".join(lines)

if __name__ == "__main__":
    order_id = input("Enter production order ID: ")
    result = diagnose_production_order(order_id)
    print(summarize_diagnosis(result))