import pandas as pd
import os


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
# 2. DATA CLEANING
# ============================================================

# Convert date/time columns into proper datetime format

orders["order_time"] = pd.to_datetime(orders["order_time"])
orders["promised_time"] = pd.to_datetime(orders["promised_time"])
orders["actual_delivery_time"] = pd.to_datetime(
    orders["actual_delivery_time"]
)

delivery["assignment_time"] = pd.to_datetime(
    delivery["assignment_time"]
)

delivery["pickup_time"] = pd.to_datetime(
    delivery["pickup_time"]
)

delivery["delivery_time"] = pd.to_datetime(
    delivery["delivery_time"]
)

picking["pick_start"] = pd.to_datetime(
    picking["pick_start"]
)

picking["pick_end"] = pd.to_datetime(
    picking["pick_end"]
)


# Remove duplicate records

orders = orders.drop_duplicates()
inventory = inventory.drop_duplicates()
delivery = delivery.drop_duplicates()
picking = picking.drop_duplicates()
workforce = workforce.drop_duplicates()


# ============================================================
# 3. KPI CALCULATIONS
# ============================================================

# ----------------------------
# ORDER KPIs
# ----------------------------

total_orders = len(orders)

total_order_value = orders["order_value"].sum()

average_order_value = orders["order_value"].mean()

sla_breaches = orders["sla_breached"].sum()

sla_breach_rate = (
    sla_breaches / total_orders
) * 100

average_delivery_delay = (
    orders["delivery_delay_minutes"].mean()
)


# ----------------------------
# INVENTORY KPIs
# ----------------------------

total_inventory_records = len(inventory)

stockouts = (
    inventory["stockout"]
    .astype(str)
    .str.lower()
    .eq("yes")
    .sum()
)

stockout_rate = (
    stockouts / total_inventory_records
) * 100

average_inventory_accuracy = (
    inventory["inventory_accuracy_pct"].mean()
)


# ----------------------------
# DELIVERY KPIs
# ----------------------------

total_deliveries = len(delivery)

average_distance = (
    delivery["distance_km"].mean()
)

average_assignment_delay = (
    delivery["assignment_delay_minutes"].mean()
)


# ----------------------------
# PICKING KPIs
# ----------------------------

total_picking_records = len(picking)

average_pick_duration = (
    picking["pick_duration_minutes"].mean()
)

total_items_picked = (
    picking["items_picked"].sum()
)

total_items_missing = (
    picking["items_missing"].sum()
)


# ----------------------------
# WORKFORCE KPIs
# ----------------------------

total_employees = len(workforce)

total_tasks_completed = (
    workforce["tasks_completed"].sum()
)

total_tasks_pending = (
    workforce["tasks_pending"].sum()
)


# ============================================================
# 4. DISPLAY KPI RESULTS
# ============================================================

print("\n")
print("=" * 60)
print("              MACROOPS AI - KPI SUMMARY")
print("=" * 60)


print("\nORDER PERFORMANCE")
print("-" * 30)

print(f"Total Orders              : {total_orders:,}")

print(
    f"Total Order Value         : "
    f"₹{total_order_value:,.2f}"
)

print(
    f"Average Order Value       : "
    f"₹{average_order_value:,.2f}"
)

print(
    f"SLA Breaches              : "
    f"{sla_breaches:,}"
)

print(
    f"SLA Breach Rate           : "
    f"{sla_breach_rate:.2f}%"
)

print(
    f"Average Delivery Delay    : "
    f"{average_delivery_delay:.2f} minutes"
)


print("\nINVENTORY PERFORMANCE")
print("-" * 30)

print(
    f"Inventory Records         : "
    f"{total_inventory_records:,}"
)

print(
    f"Stockouts                 : "
    f"{stockouts:,}"
)

print(
    f"Stockout Rate             : "
    f"{stockout_rate:.2f}%"
)

print(
    f"Inventory Accuracy        : "
    f"{average_inventory_accuracy:.2f}%"
)


print("\nDELIVERY PERFORMANCE")
print("-" * 30)

print(
    f"Total Deliveries          : "
    f"{total_deliveries:,}"
)

print(
    f"Average Distance          : "
    f"{average_distance:.2f} km"
)

print(
    f"Average Assignment Delay  : "
    f"{average_assignment_delay:.2f} minutes"
)


print("\nPICKING PERFORMANCE")
print("-" * 30)

print(
    f"Picking Records           : "
    f"{total_picking_records:,}"
)

print(
    f"Average Pick Duration     : "
    f"{average_pick_duration:.2f} minutes"
)

print(
    f"Items Picked              : "
    f"{total_items_picked:,}"
)

print(
    f"Items Missing             : "
    f"{total_items_missing:,}"
)


print("\nWORKFORCE PERFORMANCE")
print("-" * 30)

print(
    f"Employees                 : "
    f"{total_employees:,}"
)

print(
    f"Tasks Completed           : "
    f"{total_tasks_completed:,}"
)

print(
    f"Tasks Pending             : "
    f"{total_tasks_pending:,}"
)


print("\n" + "=" * 60)
print("              KPI ANALYSIS COMPLETED")
print("=" * 60)