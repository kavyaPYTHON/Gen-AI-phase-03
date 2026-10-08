# MacroOps AI

## GenAI-Powered Fulfillment & Last-Mile Operations Intelligence Platform

MacroOps AI is a GenAI-powered operations intelligence platform designed for quick-commerce, e-commerce and retail fulfillment environments.

The platform combines operational analytics, exception detection, SLA risk prediction, RAG-based knowledge assistance and GenAI-powered operational support to help teams move from reactive operations to proactive decision-making.

---

## Problem Statement

Modern fulfillment and last-mile operations generate large amounts of operational data across orders, inventory, picking, workforce and delivery activities.

Operations teams often depend on dashboards, spreadsheets and manual investigation to identify delays, SLA breaches, inventory issues and operational exceptions.

MacroOps AI addresses this problem by bringing operational monitoring, predictive intelligence and GenAI assistance into a unified platform.

---

## Objectives

- Monitor fulfillment and last-mile operations.
- Track important operational KPIs.
- Detect operational exceptions.
- Identify SLA breaches and delivery delays.
- Predict SLA risk levels.
- Provide root-cause-oriented operational insights.
- Provide SOP-based knowledge assistance using RAG.
- Support frontline employees with AI assistance.
- Provide recommendations for operational decision-making.
- Improve operational visibility and decision speed.

---

## Main Features

### 1. Executive Dashboard

Provides an overall view of operational performance using key metrics such as:

- Total orders
- SLA breach rate
- Average delivery delay
- Inventory accuracy
- Stockout rate
- Average picking time
- Pending workforce tasks
- Operational exceptions

### 2. SLA Monitoring

Monitors delivery performance and SLA breaches.

The system also classifies orders into:

- Low Risk
- Medium Risk
- High Risk

based on delivery delay.

### 3. Exception Management

Automatically identifies operational exceptions including:

- SLA breaches
- Inventory stockouts
- Delivery assignment delays
- Picking delays
- Workforce backlog

### 4. Inventory Intelligence

Provides inventory-related operational insights including:

- Inventory records
- Stockouts
- Inventory accuracy
- Inventory-related exceptions

### 5. Delivery Analytics

Analyzes delivery operations including:

- Delivery distance
- Rider assignment delay
- Delivery performance
- SLA-related issues

### 6. Picking Analytics

Provides insights into:

- Pick duration
- Items picked
- Missing items
- Picking productivity

### 7. Workforce Analytics

Monitors workforce activity including:

- Completed tasks
- Pending tasks
- Workforce backlog

### 8. RAG Knowledge Assistant

Uses project-level operational SOP documents as a knowledge source.

The current prototype includes a delivery delay SOP covering:

- Issue identification
- Delivery assignment checks
- Delivery condition checks
- Order prioritization
- Corrective action
- Resolution recording
- Preventive action

### 9. AI Operations Copilot

The GenAI Copilot combines:

- Operational data
- KPI information
- Exception information
- SOP knowledge

to provide natural-language operational assistance.

### 10. Frontline AI Assistant

Provides simple operational guidance for frontline employees such as:

- Store staff
- Pickers
- Packers
- Delivery coordinators
- Operations executives

---

## Technology Stack

- Python
- Pandas
- Streamlit
- Plotly
- OpenAI API
- Retrieval-Augmented Generation (RAG)
- CSV operational datasets
- GitHub

---

## Project Structure

```text
MacroOps-AI/
│
├── data/
│   ├── delivery.csv
│   ├── inventory.csv
│   ├── orders.csv
│   ├── picking.csv
│   ├── workforce.csv
│   ├── exceptions.csv
│   └── README.txt
│
├── knowledge_base/
│   └── delivery_delay_sop.txt
│
├── app/
│   ├── app.py
│   ├── data_exploration.py
│   ├── analytics.py
│   ├── exceptions.py
│   ├── rag.py
│   ├── sla_prediction.py
│   ├── frontline_ai.py
│   └── business_impact.py
│
└── README.md