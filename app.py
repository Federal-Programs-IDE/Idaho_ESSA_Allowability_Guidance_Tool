# set up the code to return what I want

import pandas as pd
from sentence_transformers import SentenceTransformer, util
import json
import torch
import os
os.environ['HF_HUB_OFFLINE'] = '1'

# Include Logo so we look official
#st.image("logo.png", width=200)

def get_guidance(grant, expense_type):
    df = pd.read_csv("allowable_use_mapping.csv").fillna("")

    # Return all rows if School Improvement or V-B selected
    if grant in ['Title I-A SI','Title V-B']:
        result = df[df['Grant'] == grant][['Guidance','Status']]
        return result.apply(lambda row: f"{row['Guidance']}:row{'Status'}", axis=1).tolist()

    # Return for cases where the expense applies to all grants
    all_match = df[(df['Grant'] == 'All') & (df['Expense Type'].isin(expense_type))]

    grant_match = df[(df['Grant'] == grant) & (df['Expense Type'].isin(expense_type))]

    result = pd.concat([all_match, grant_match])

    if not result.empty:
        return "\n\n".join(result.apply(
            lambda row: f"{row['Guidance']}: {row['Status']}" if row['Guidance'] else row['Status'],
            axis=1
        ).tolist())
        return "\n\n".join(formatted_list)

    return "Error: Please Try Again"


# Load pre-computed embeddings
with open('embeddings.json', 'r') as f:
    data = json.load(f)

expense_types = data['expense_types']
embeddings = torch.tensor(data['embeddings'])

# Load model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def match_expense(user_input):
    # Encode user input
    user_embedding = model.encode(user_input)
    
    # Calculate similarities
    similarities = util.cos_sim(user_embedding, embeddings)[0]
    
    # Get top match
    ranked_idx = similarities.argsort(descending=True)[:10]
    return [expense_types[i] for i in ranked_idx]

# User input
import streamlit as st

st.title("Grant Expense Guidance Lookup")

grant = st.selectbox("Select Title Grant", [
    "Title I-A", "Title I-A SI", "Title I-C", "Title I-D Subpart 1",
    "Title I-D Subpart 2", "Title I-D", "Title II-A", "Title III-A",
    "Title III-A Immigrant", "Title IV-A", "Title V-B", "Title IX-A",
    "Equitable Services", "Parent Engagement"
])

expense_description = st.text_area("Describe the expense")

if st.button("Get Guidance"):
    if not grant or not expense_description:
        st.error("Please fill in all fields")
    else:
        matched_expense = match_expense(expense_description)
        result = get_guidance(grant, matched_expense)
        st.markdown(result)
