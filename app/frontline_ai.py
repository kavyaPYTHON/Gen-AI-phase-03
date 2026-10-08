import os
import pandas as pd
from openai import OpenAI

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORDERS_FILE = os.path.join(BASE_DIR, "data", "orders.csv")
DELIVERY_FILE = os.path.join(BASE_DIR, "data", "delivery.csv")
INVENTORY_FILE = os.path.join(BASE_DIR, "data", "inventory.csv")
PICKING_FILE = os.path.join(BASE_DIR, "data", "picking.csv")
WORKFORCE_FILE = os.path.join(BASE_DIR, "data", "workforce.csv")


def load_frontline_data():

    data = {}

    files = {
        "orders": ORDERS_FILE,
        "delivery": DELIVERY_FILE,
        "inventory": INVENTORY_FILE,
        "picking": PICKING_FILE,
        "workforce": WORKFORCE_FILE
    }

    for name, filepath in files.items():

        try:
            data[name] = pd.read_csv(filepath)

        except Exception:
            data[name] = pd.DataFrame()

    return data


def build_frontline_context():

    data = load_frontline_data()

    orders = data["orders"]
    delivery = data["delivery"]
    inventory = data["inventory"]
    picking = data["picking"]
    workforce = data["workforce"]

    context = []

    # Orders
    if not orders.empty:

        if "order_id" in orders.columns:
            context.append(
                f"Total orders: {len(orders)}"
            )

        if "sla_breached" in orders.columns:
            breaches = orders["sla_breached"].sum()

            context.append(
                f"SLA breached orders: {int(breaches)}"
            )

        if "delivery_delay_minutes" in orders.columns:
            avg_delay = orders[
                "delivery_delay_minutes"
            ].mean()

            context.append(
                f"Average delivery delay: {avg_delay:.2f} minutes"
            )

    # Delivery
    if not delivery.empty:

        if "assignment_delay_minutes" in delivery.columns:

            avg_assignment = delivery[
                "assignment_delay_minutes"
            ].mean()

            context.append(
                f"Average rider assignment delay: "
                f"{avg_assignment:.2f} minutes"
            )

    # Inventory
    if not inventory.empty:

        if "stockout" in inventory.columns:

            stockouts = inventory[
                "stockout"
            ].astype(str).str.lower().isin(
                ["1", "true", "yes", "y"]
            ).sum()

            context.append(
                f"Inventory stockouts: {int(stockouts)}"
            )

    # Picking
    if not picking.empty:

        if "pick_duration_minutes" in picking.columns:

            avg_pick = picking[
                "pick_duration_minutes"
            ].mean()

            context.append(
                f"Average picking duration: "
                f"{avg_pick:.2f} minutes"
            )

    # Workforce
    if not workforce.empty:

        if "status" in workforce.columns:

            pending = workforce[
                workforce["status"]
                .astype(str)
                .str.lower()
                .isin(["pending", "open"])
            ]

            context.append(
                f"Pending workforce tasks: {len(pending)}"
            )

    return "\n".join(context)


def ask_frontline_ai(question):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "OpenAI API key is not available. "
            "Please set OPENAI_API_KEY in the terminal."
        )

    client = OpenAI(api_key=api_key)

    operational_context = build_frontline_context()

    system_prompt = """
You are MacroOps AI Frontline Assistant.

You support frontline employees such as:
- Store staff
- Pickers
- Packers
- Delivery coordinators
- Operations executives

Your job is to provide simple, practical and safe operational guidance.

Use the operational data provided to understand the current situation.

Rules:
1. Give clear step-by-step instructions.
2. Keep responses concise.
3. Highlight urgent operational risks.
4. Do not invent operational data.
5. Do not claim that an action has actually been performed.
6. Escalate serious or repeated issues to the operations manager.
7. Human approval is required before major operational actions.
"""

    user_prompt = f"""
Current MacroOps AI operational context:

{operational_context}

Frontline employee question:

{question}

Provide:
1. What is happening
2. What the employee should do
3. When to escalate
"""

    try:

        response = client.responses.create(
            model="gpt-6-luna",
            instructions=system_prompt,
            input=user_prompt
        )

        return response.output_text

    except Exception as e:

        return f"Frontline AI error: {str(e)}"


if __name__ == "__main__":

    print("\nMACROOPS AI - FRONTLINE ASSISTANT")
    print("---------------------------------")

    question = input(
        "Enter a frontline operational question: "
    )

    answer = ask_frontline_ai(question)

    print("\nAI RESPONSE")
    print("-----------")
    print(answer)