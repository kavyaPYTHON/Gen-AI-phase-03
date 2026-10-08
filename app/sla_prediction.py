import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDERS_FILE = os.path.join(BASE_DIR, "data", "orders.csv")


def predict_sla_risk():

    df = pd.read_csv(ORDERS_FILE)

    df["delivery_delay_minutes"] = pd.to_numeric(
        df["delivery_delay_minutes"],
        errors="coerce"
    ).fillna(0)

    def classify_risk(delay):

        if delay >= 10:
            return "High"
        elif delay >= 5:
            return "Medium"
        else:
            return "Low"

    df["sla_risk"] = df["delivery_delay_minutes"].apply(classify_risk)

    return df


if __name__ == "__main__":

    result = predict_sla_risk()

    print("\nSLA RISK PREDICTION")
    print("-------------------")

    print(result["sla_risk"].value_counts())

    print("\nSample Predictions:")

    print(
        result[
            [
                "order_id",
                "delivery_delay_minutes",
                "sla_breached",
                "sla_risk"
            ]
        ].head(10)
    )