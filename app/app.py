import os
import pandas as pd
import streamlit as st
import plotly.express as px

from openai import OpenAI
from rag import retrieve_relevant_sop
from sla_prediction import predict_sla_risk
from frontline_ai import ask_frontline_ai
from business_impact import calculate_business_impact


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MacroOps AI",
    page_icon="🚚",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():

    files = {
        "orders": "orders.csv",
        "inventory": "inventory.csv",
        "delivery": "delivery.csv",
        "picking": "picking.csv",
        "workforce": "workforce.csv",
        "exceptions": "exceptions.csv"
    }

    data = {}

    for name, filename in files.items():

        path = os.path.join(DATA_DIR, filename)

        try:
            data[name] = pd.read_csv(path)
        except Exception:
            data[name] = pd.DataFrame()

    return data


data = load_data()

orders = data["orders"]
inventory = data["inventory"]
delivery = data["delivery"]
picking = data["picking"]
workforce = data["workforce"]
exceptions = data["exceptions"]


# ============================================================
# SAFE FUNCTIONS
# ============================================================

def safe_mean(df, column):

    if column not in df.columns or df.empty:
        return 0

    values = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    if values.dropna().empty:
        return 0

    return values.mean()


def safe_sum(df, column):

    if column not in df.columns or df.empty:
        return 0

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0).sum()


def safe_count(df):

    if df.empty:
        return 0

    return len(df)


def get_inventory_accuracy():

    if inventory.empty:
        return 0

    for column in [
        "inventory_accuracy",
        "accuracy"
    ]:

        if column in inventory.columns:

            value = pd.to_numeric(
                inventory[column],
                errors="coerce"
            ).mean()

            return value

    # If accuracy is represented as a percentage/status,
    # return the known project value calculation where possible.
    return 0


def get_stockouts():

    if inventory.empty:
        return 0

    for column in [
        "stockout",
        "stockout_flag",
        "is_stockout"
    ]:

        if column in inventory.columns:

            values = inventory[column].astype(str).str.lower()

            return values.isin(
                ["1", "true", "yes", "y"]
            ).sum()

    return 0


def get_pending_tasks():

    if workforce.empty:
        return 0

    if "status" not in workforce.columns:
        return 0

    status = workforce["status"].astype(str).str.lower()

    return status.isin(
        ["pending", "open"]
    ).sum()


def get_avg_pick_time():

    for column in [
        "pick_duration_minutes",
        "pick_duration",
        "picking_duration_minutes"
    ]:

        if column in picking.columns:
            return safe_mean(
                picking,
                column
            )

    return 0


def get_avg_delivery_delay():

    if "delivery_delay_minutes" in orders.columns:

        return safe_mean(
            orders,
            "delivery_delay_minutes"
        )

    return 0


def get_sla_breaches():

    if "sla_breached" in orders.columns:

        return int(
            safe_sum(
                orders,
                "sla_breached"
            )
        )

    return 0


def get_sla_breach_rate():

    total = len(orders)

    if total == 0:
        return 0

    return (
        get_sla_breaches()
        / total
        * 100
    )


# ============================================================
# OPERATIONAL CONTEXT
# ============================================================

def build_operational_context():

    context = []

    context.append(
        f"Total orders: {len(orders)}"
    )

    context.append(
        f"SLA breaches: {get_sla_breaches()}"
    )

    context.append(
        f"SLA breach rate: "
        f"{get_sla_breach_rate():.2f}%"
    )

    context.append(
        f"Average delivery delay: "
        f"{get_avg_delivery_delay():.2f} minutes"
    )

    context.append(
        f"Inventory accuracy: "
        f"{get_inventory_accuracy():.2f}%"
    )

    context.append(
        f"Inventory stockouts: "
        f"{get_stockouts()}"
    )

    context.append(
        f"Average pick time: "
        f"{get_avg_pick_time():.2f} minutes"
    )

    context.append(
        f"Pending workforce tasks: "
        f"{get_pending_tasks()}"
    )

    context.append(
        f"Operational exceptions: "
        f"{len(exceptions)}"
    )

    return "\n".join(context)


# ============================================================
# GENAI OPERATIONS COPILOT
# ============================================================

def ask_genai(question):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:

        return (
            "OpenAI API key is not available in this terminal. "
            "Please set OPENAI_API_KEY and restart Streamlit."
        )

    try:

        client = OpenAI(
            api_key=api_key
        )

        operational_context = (
            build_operational_context()
        )

        sop_context = retrieve_relevant_sop(
            question
        )

        system_prompt = """
You are MacroOps AI, an operations intelligence assistant.

You support fulfillment and last-mile operations.

Use the provided operational data and SOP context.

Your responsibilities:
- Explain operational problems.
- Identify possible root causes.
- Highlight risks.
- Recommend practical actions.
- Use SOP information when relevant.
- Never invent operational data.
- Never claim that an action has already been performed.
- Major operational actions require human approval.

Give clear and concise answers suitable for an operations manager.
"""

        user_prompt = f"""
CURRENT OPERATIONAL DATA:

{operational_context}


RELEVANT SOP / KNOWLEDGE:

{sop_context}


USER QUESTION:

{question}


Provide:
1. Situation
2. Likely cause
3. Recommended action
4. Escalation guidance if required
"""

        response = client.responses.create(
            model="gpt-6-luna",
            instructions=system_prompt,
            input=user_prompt
        )

        return response.output_text

    except Exception as e:

        return f"GenAI error: {str(e)}"


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚚 MacroOps AI")

st.sidebar.markdown(
    "### Operations Intelligence Platform"
)

st.sidebar.write(
    "GenAI-powered fulfillment and "
    "last-mile operations intelligence."
)

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Dashboard",
        "SLA Monitoring",
        "Exception Management",
        "Inventory Intelligence",
        "Delivery Analytics",
        "Picking Analytics",
        "Workforce Analytics",
        "Business Impact",
        "Frontline AI Assistant",
        "AI Operations Copilot"
    ]
)


# ============================================================
# HEADER
# ============================================================

st.title("🚚 MacroOps AI")

st.caption(
    "GenAI-Powered Fulfillment & Last-Mile "
    "Operations Intelligence Platform"
)

st.divider()


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.header("📊 Executive Operations Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Orders",
            f"{len(orders):,}"
        )

    with col2:
        st.metric(
            "SLA Breach Rate",
            f"{get_sla_breach_rate():.2f}%"
        )

    with col3:
        st.metric(
            "Avg Delivery Delay",
            f"{get_avg_delivery_delay():.2f} min"
        )

    with col4:
        st.metric(
            "Inventory Accuracy",
            f"{get_inventory_accuracy():.2f}%"
        )

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            "Stockouts",
            f"{get_stockouts():,}"
        )

    with col6:
        st.metric(
            "Avg Pick Time",
            f"{get_avg_pick_time():.2f} min"
        )

    with col7:
        st.metric(
            "Pending Tasks",
            f"{get_pending_tasks():,}"
        )

    with col8:
        st.metric(
            "Exceptions",
            f"{len(exceptions):,}"
        )

    st.subheader("Operational Overview")

    overview = pd.DataFrame({
        "Metric": [
            "SLA Breaches",
            "Stockouts",
            "Pending Tasks",
            "Exceptions"
        ],
        "Count": [
            get_sla_breaches(),
            get_stockouts(),
            get_pending_tasks(),
            len(exceptions)
        ]
    })

    fig = px.bar(
        overview,
        x="Metric",
        y="Count",
        title="Key Operational Issues"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# SLA MONITORING
# ============================================================

elif page == "SLA Monitoring":

    st.header("⏱️ SLA Monitoring")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Orders",
            f"{len(orders):,}"
        )

    with col2:
        st.metric(
            "SLA Breaches",
            f"{get_sla_breaches():,}"
        )

    with col3:
        st.metric(
            "SLA Breach Rate",
            f"{get_sla_breach_rate():.2f}%"
        )

    st.subheader("🔮 SLA Risk Prediction")

    try:

        prediction_df = predict_sla_risk()

        risk_counts = (
            prediction_df["sla_risk"]
            .value_counts()
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🟢 Low Risk",
                f"{int(risk_counts.get('Low', 0)):,}"
            )

        with col2:
            st.metric(
                "🟡 Medium Risk",
                f"{int(risk_counts.get('Medium', 0)):,}"
            )

        with col3:
            st.metric(
                "🔴 High Risk",
                f"{int(risk_counts.get('High', 0)):,}"
            )

        risk_chart = (
            risk_counts
            .reset_index()
        )

        risk_chart.columns = [
            "Risk Level",
            "Orders"
        ]

        fig = px.bar(
            risk_chart,
            x="Risk Level",
            y="Orders",
            title="SLA Risk Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader(
            "Sample SLA Risk Predictions"
        )

        display_columns = [
            column for column in [
                "order_id",
                "delivery_delay_minutes",
                "sla_breached",
                "sla_risk"
            ]
            if column in prediction_df.columns
        ]

        st.dataframe(
            prediction_df[
                display_columns
            ].head(20),
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"SLA prediction error: {e}"
        )


# ============================================================
# EXCEPTION MANAGEMENT
# ============================================================

elif page == "Exception Management":

    st.header("🚨 Exception Management")

    st.metric(
        "Total Exceptions",
        f"{len(exceptions):,}"
    )

    if not exceptions.empty:

        st.dataframe(
            exceptions.head(100),
            use_container_width=True
        )

        # Try to identify a useful category column
        category_column = None

        for column in [
            "exception_type",
            "type",
            "category",
            "exception"
        ]:

            if column in exceptions.columns:
                category_column = column
                break

        if category_column:

            counts = (
                exceptions[
                    category_column
                ]
                .value_counts()
                .reset_index()
            )

            counts.columns = [
                "Exception Type",
                "Count"
            ]

            fig = px.bar(
                counts,
                x="Exception Type",
                y="Count",
                title="Exception Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.info(
            "No exceptions available."
        )


# ============================================================
# INVENTORY INTELLIGENCE
# ============================================================

elif page == "Inventory Intelligence":

    st.header("📦 Inventory Intelligence")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Inventory Records",
            f"{len(inventory):,}"
        )

    with col2:
        st.metric(
            "Stockouts",
            f"{get_stockouts():,}"
        )

    with col3:
        st.metric(
            "Inventory Accuracy",
            f"{get_inventory_accuracy():.2f}%"
        )

    if not inventory.empty:

        st.subheader(
            "Inventory Data"
        )

        st.dataframe(
            inventory.head(100),
            use_container_width=True
        )


# ============================================================
# DELIVERY ANALYTICS
# ============================================================

elif page == "Delivery Analytics":

    st.header("🚚 Delivery Analytics")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Deliveries",
            f"{len(delivery):,}"
        )

    with col2:

        assignment_delay = 0

        for column in [
            "assignment_delay_minutes",
            "rider_assignment_delay_minutes"
        ]:

            if column in delivery.columns:

                assignment_delay = safe_mean(
                    delivery,
                    column
                )

                break

        st.metric(
            "Avg Assignment Delay",
            f"{assignment_delay:.2f} min"
        )

    if not delivery.empty:

        st.dataframe(
            delivery.head(100),
            use_container_width=True
        )


# ============================================================
# PICKING ANALYTICS
# ============================================================

elif page == "Picking Analytics":

    st.header("🛒 Picking Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Picking Records",
            f"{len(picking):,}"
        )

    with col2:
        st.metric(
            "Average Pick Time",
            f"{get_avg_pick_time():.2f} min"
        )

    if not picking.empty:

        st.dataframe(
            picking.head(100),
            use_container_width=True
        )


# ============================================================
# WORKFORCE ANALYTICS
# ============================================================

elif page == "Workforce Analytics":

    st.header("👷 Workforce Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Workforce Records",
            f"{len(workforce):,}"
        )

    with col2:
        st.metric(
            "Pending Tasks",
            f"{get_pending_tasks():,}"
        )

    if not workforce.empty:

        st.dataframe(
            workforce.head(100),
            use_container_width=True
        )


# ============================================================
# BUSINESS IMPACT
# ============================================================

elif page == "Business Impact":

    st.header("📈 Business Impact Analysis")

    try:

        impact = calculate_business_impact()

        metrics = list(
            impact.items()
        )

        for i in range(
            0,
            len(metrics),
            4
        ):

            columns = st.columns(4)

            for j, (name, value) in enumerate(
                metrics[i:i + 4]
            ):

                with columns[j]:

                    if isinstance(
                        value,
                        float
                    ):

                        display_value = (
                            f"{value:.2f}"
                        )

                    else:

                        display_value = (
                            f"{value:,}"
                            if isinstance(
                                value,
                                (int, float)
                            )
                            else str(value)
                        )

                    st.metric(
                        name,
                        display_value
                    )

        st.subheader(
            "Operational Improvement Areas"
        )

        improvement = pd.DataFrame({
            "Business Area": [
                "SLA Performance",
                "Exception Management",
                "Inventory Accuracy",
                "Picking Productivity",
                "Workforce Visibility",
                "Decision Speed"
            ],
            "MacroOps AI Support": [
                "SLA monitoring and risk prediction",
                "Automated exception identification",
                "Inventory intelligence",
                "Picking analytics",
                "Workforce analytics",
                "GenAI operational assistance"
            ]
        })

        st.dataframe(
            improvement,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Business impact error: {e}"
        )


# ============================================================
# FRONTLINE AI ASSISTANT
# ============================================================

elif page == "Frontline AI Assistant":

    st.header("🧑‍💼 Frontline AI Assistant")

    st.write(
        "Ask practical operational questions "
        "related to orders, delivery, picking, "
        "inventory or workforce activities."
    )

    question = st.text_area(
        "Enter your operational question:",
        placeholder=(
            "Example: What should I do if "
            "a customer order is delayed?"
        )
    )

    if st.button(
        "🤖 Get AI Assistance"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Generating frontline guidance..."
            ):

                answer = ask_frontline_ai(
                    question
                )

            st.subheader(
                "AI Guidance"
            )

            st.write(answer)

            st.info(
                "Operational actions should be "
                "reviewed and approved by the "
                "responsible manager."
            )


# ============================================================
# AI OPERATIONS COPILOT
# ============================================================

elif page == "AI Operations Copilot":

    st.header("🤖 AI Operations Copilot")

    st.write(
        "Ask questions about current operations, "
        "SLA performance, exceptions, delivery "
        "delays, inventory or operational SOPs."
    )

    question = st.text_area(
        "Ask MacroOps AI:",
        placeholder=(
            "Example: Why are SLA breaches high "
            "and what actions should operations take?"
        )
    )

    if st.button(
        "🚀 Ask MacroOps AI"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Analyzing operational data and SOP..."
            ):

                answer = ask_genai(
                    question
                )

            st.subheader(
                "MacroOps AI Response"
            )

            st.write(answer)

            st.info(
                "AI recommendations are decision "
                "support and require human approval "
                "before major operational actions."
            )

    st.divider()

    st.subheader(
        "Current Operational Context"
    )

    st.code(
        build_operational_context()
    )