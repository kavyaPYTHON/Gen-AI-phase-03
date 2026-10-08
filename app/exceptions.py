import pandas as pd
import os


# ============================================================
# MACROOPS AI - EXCEPTION MANAGEMENT
# ============================================================


# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_FOLDER = "../data"

orders = pd.read_csv(
    os.path.join(DATA_FOLDER, "orders.csv")
)

inventory = pd.read_csv(
    os.path.join(DATA_FOLDER, "inventory.csv")
)

delivery = pd.read_csv(
    os.path.join(DATA_FOLDER, "delivery.csv")
)

picking = pd.read_csv(
    os.path.join(DATA_FOLDER, "picking.csv")
)

workforce = pd.read_csv(
    os.path.join(DATA_FOLDER, "workforce.csv")
)


# ============================================================
# 2. CREATE EMPTY EXCEPTION LIST
# ============================================================

exceptions = []


# ============================================================
# 3. SLA BREACH EXCEPTIONS
# ============================================================

sla_values = (
    orders["sla_breached"]
    .astype(str)
    .str.strip()
    .str.lower()
)

sla_orders = orders[
    sla_values.isin(["yes", "true", "1", "y"])
]


for _, row in sla_orders.head(1000).iterrows():

    exceptions.append({
        "type": "SLA Breach",
        "id": row["order_id"],
        "severity": "HIGH",
        "reason": (
            f"Delivery delay of "
            f"{row['delivery_delay_minutes']:.1f} minutes"
        ),
        "recommended_action":
            "Prioritize order and review rider allocation"
    })


# ============================================================
# 4. INVENTORY STOCKOUT EXCEPTIONS
# ============================================================

stockout_values = (
    inventory["stockout"]
    .astype(str)
    .str.strip()
    .str.lower()
)

stockout_inventory = inventory[
    stockout_values.isin(["yes", "true", "1", "y"])
]


for index, row in stockout_inventory.head(1000).iterrows():

    # Find the best available identifier
    if "sku" in inventory.columns:

        record_id = row["sku"]

    elif "product_id" in inventory.columns:

        record_id = row["product_id"]

    elif "inventory_id" in inventory.columns:

        record_id = row["inventory_id"]

    elif "item_id" in inventory.columns:

        record_id = row["item_id"]

    else:

        # If there is no product identifier,
        # use the row number
        record_id = index

    exceptions.append({
        "type": "Inventory Stockout",
        "id": record_id,
        "severity": "HIGH",
        "reason":
            "Product is currently out of stock",
        "recommended_action":
            "Trigger inventory replenishment"
    })


# ============================================================
# 5. DELIVERY ASSIGNMENT DELAY EXCEPTIONS
# ============================================================

high_assignment_delay = delivery[
    delivery["assignment_delay_minutes"] > 15
]


for _, row in high_assignment_delay.head(1000).iterrows():

    exceptions.append({
        "type": "Delivery Assignment Delay",
        "id": row["order_id"],
        "severity": "MEDIUM",
        "reason": (
            f"Assignment delay of "
            f"{row['assignment_delay_minutes']:.1f} minutes"
        ),
        "recommended_action":
            "Check rider availability and reallocate if required"
    })


# ============================================================
# 6. PICKING DELAY EXCEPTIONS
# ============================================================

# Calculate the 90th percentile.
# This identifies the slowest approximately 10% of
# picking operations.

pick_threshold = (
    picking["pick_duration_minutes"]
    .quantile(0.90)
)


slow_picking = picking[
    picking["pick_duration_minutes"] > pick_threshold
]


for _, row in slow_picking.head(1000).iterrows():

    exceptions.append({
        "type": "Picking Delay",
        "id": row["order_id"],
        "severity": "MEDIUM",
        "reason": (
            f"Pick duration of "
            f"{row['pick_duration_minutes']:.1f} minutes"
        ),
        "recommended_action":
            "Review picker workload and process delays"
    })


# ============================================================
# 7. WORKFORCE BACKLOG EXCEPTIONS
# ============================================================

workforce_threshold = (
    workforce["tasks_pending"]
    .quantile(0.90)
)


high_pending = workforce[
    workforce["tasks_pending"] > workforce_threshold
]


for _, row in high_pending.head(1000).iterrows():

    exceptions.append({
        "type": "Workforce Backlog",
        "id": row["employee_id"],
        "severity": "MEDIUM",
        "reason": (
            f"{row['tasks_pending']} pending tasks"
        ),
        "recommended_action":
            "Rebalance workload across available workforce"
    })


# ============================================================
# 8. CONVERT EXCEPTIONS INTO DATAFRAME
# ============================================================

exceptions_df = pd.DataFrame(exceptions)


# ============================================================
# 9. DISPLAY SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("              MACROOPS AI - EXCEPTION MANAGEMENT")
print("=" * 70)


print(
    f"\nTotal Exceptions Detected: "
    f"{len(exceptions_df):,}"
)


# ============================================================
# 10. EXCEPTION TYPE SUMMARY
# ============================================================

print("\nException Type Summary")
print("-" * 40)

if not exceptions_df.empty:

    print(
        exceptions_df["type"]
        .value_counts()
    )

else:

    print("No exceptions detected.")


# ============================================================
# 11. SEVERITY SUMMARY
# ============================================================

print("\nSeverity Summary")
print("-" * 40)

if not exceptions_df.empty:

    print(
        exceptions_df["severity"]
        .value_counts()
    )

else:

    print("No severity information available.")


# ============================================================
# 12. DISPLAY TOP EXCEPTIONS
# ============================================================

print("\nTop 20 Operational Exceptions")
print("-" * 70)

if not exceptions_df.empty:

    print(
        exceptions_df
        .head(20)
        .to_string(index=False)
    )

else:

    print("No operational exceptions detected.")


# ============================================================
# 13. SAVE EXCEPTION REPORT
# ============================================================

output_file = "../data/exceptions.csv"


exceptions_df.to_csv(
    output_file,
    index=False
)


print("\nException report saved to:")
print(output_file)


# ============================================================
# 14. COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("              EXCEPTION ANALYSIS COMPLETED")
print("=" * 70)