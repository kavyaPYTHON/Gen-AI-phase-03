import pandas as pd
import os

# Location of our data files
data_folder = "../data"

# List of datasets
files = [
    "orders.csv",
    "inventory.csv",
    "delivery.csv",
    "picking.csv",
    "workforce.csv"
]

for file in files:

    print("\n" + "=" * 60)
    print(f"DATASET: {file}")
    print("=" * 60)

    # Read CSV file
    file_path = os.path.join(data_folder, file)
    df = pd.read_csv(file_path)

    # Number of rows and columns
    print("\nShape:")
    print(df.shape)

    # Column names
    print("\nColumns:")
    print(df.columns.tolist())

    # Data types
    print("\nData Types:")
    print(df.dtypes)

    # Missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # First 5 records
    print("\nFirst 5 Records:")
    print(df.head())