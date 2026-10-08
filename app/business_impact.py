import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORDERS_FILE = os.path.join(BASE_DIR, "data", "orders.csv")
INVENTORY_FILE = os.path.join(BASE_DIR, "data", "inventory.csv")
PICKING_FILE = os.path.join(BASE_DIR, "data", "picking.csv")
WORKFORCE_FILE = os.path.join(BASE_DIR, "data", "workforce.csv")
EXCEPTIONS_FILE = os.path.join(BASE_DIR, "data", "exceptions.csv")


def calculate_business_impact():

    orders = pd.read_csv(ORDERS_FILE)
    inventory = pd.read_csv(INVENTORY_FILE)
    picking = pd.read_csv(PICKING_FILE)
    workforce = pd.read_csv(WORKFORCE_FILE)

    # -----------------------------
    # ORDER PERFORMANCE
    # -----------------------------

    total_orders = len(orders)

    sla_breaches = 0

    if "sla_breached" in orders.columns:
        sla_breaches = int(
            pd.to_numeric(
                orders["sla_breached"],
                errors="coerce"
            ).fillna(0).sum()
        )

    sla_breach_rate = (
        sla_breaches / total_orders * 100
        if total_orders > 0
        else 0
    )

    avg_delivery_delay = 0

    if "delivery_delay_minutes" in orders.columns:
        avg_delivery_delay = pd.to_numeric(
            orders["delivery_delay_minutes"],
            errors="coerce"
        ).mean()

    # -----------------------------
    # INVENTORY
    # -----------------------------

    inventory_accuracy = 0

    if "inventory_accuracy" in inventory.columns:

        inventory_accuracy = pd.to_numeric(
            inventory["inventory_accuracy"],
            errors="coerce"
        ).mean()

    elif "accuracy" in inventory.columns:

        inventory_accuracy = pd.to_numeric(
            inventory["accuracy"],
            errors="coerce"
        ).mean()

    # -----------------------------
    # PICKING
    # -----------------------------

    avg_pick_time = 0

    if "pick_duration_minutes" in picking.columns:

        avg_pick_time = pd.to_numeric(
            picking["pick_duration_minutes"],
            errors="coerce"
        ).mean()

    # -----------------------------
    # WORKFORCE
    # -----------------------------

    pending_tasks = 0

    if "status" in workforce.columns:

        pending_tasks = workforce[
            workforce["status"]
            .astype(str)
            .str.lower()
            .isin(["pending", "open"])
        ].shape[0]

    # -----------------------------
    # EXCEPTIONS
    # -----------------------------

    exception_count = 0

    if os.path.exists(EXCEPTIONS_FILE):

        exceptions = pd.read_csv(EXCEPTIONS_FILE)

        exception_count = len(exceptions)

    # -----------------------------
    # BUSINESS IMPACT SUMMARY
    # -----------------------------

    return {
        "Total Orders": total_orders,
        "SLA Breaches": sla_breaches,
        "SLA Breach Rate (%)": round(sla_breach_rate, 2),
        "Average Delivery Delay (min)": round(
            avg_delivery_delay, 2
        ),
        "Inventory Accuracy (%)": round(
            inventory_accuracy, 2
        ),
        "Average Pick Time (min)": round(
            avg_pick_time, 2
        ),
        "Pending Workforce Tasks": pending_tasks,
        "Operational Exceptions": exception_count
    }


if __name__ == "__main__":

    print("\nMACROOPS AI - BUSINESS IMPACT ANALYSIS")
    print("---------------------------------------")

    impact = calculate_business_impact()

    for metric, value in impact.items():

        print(f"{metric}: {value}")