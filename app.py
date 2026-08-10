import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 1. Load Embeddings JSON
with open("embeddings.json", "r") as f:
    embeddings_data = f.read()

# 2. Load CSV and convert to JSON format for JavaScript
df = pd.read_csv("allowable_use_mapping.csv")
# Maps CSV columns to the exact field names your JavaScript expects
csv_dict = [
    {
        "grant": str(row.get("grant", "")),
        "expenseType": str(row.get("Expense Type", "")),
        "status": str(row.get("Status", "")),
        "guidance": str(row.get("Guidance", ""))
    }
    for _, row in df.iterrows()
]
csv_json_data = json.dumps(csv_dict)

# 3. Load HTML File
with open("grant_lookup_tool.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# 4. Inject BOTH datasets into HTML
injected_html = html_code.replace("__EMBEDDINGS_DATA__", embeddings_data)
injected_html = injected_html.replace("__CSV_DATA__", csv_json_data)

# 5. Render
components.html(injected_html, height=600)
