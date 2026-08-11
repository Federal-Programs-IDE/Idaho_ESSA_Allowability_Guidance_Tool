# set up the code to return what I want

import pandas as pd
from sentence_transformers import SentenceTransformer, util
import json
import torch
import os
import streamlit as st
os.environ['HF_HUB_OFFLINE'] = '1'

# Load custom blocklist
with open('blocked_words.txt', 'r') as f:
    custom_words = [word.strip() for word in f.readlines()]

# Include Logo so we look official
col1, col2, col3 = st.columns(3)
with col2:
    st.image("SDE-logo.jpg", width=200)

PRIMARY_COLOR = "#FFFFFF" # white
BG_COLOR = "#024D99" # blue
SECONDARY_BG = "#002742" # navy
TEXT_COLOR = "#FFFFFF" # white

# Instructions
st.markdown("""
<div style="background-color: {SECONDARY_BG}; padding: 20px; border-radius: 5px; width: 100%; box-sizing: border-box;">
<p style="color: {TEXT_COLOR}; text-align: center; margin: 0;">Select the grant you are looking to use funds from and enter the purchase you wish to make. Relevant guidance will appear below</p>
</div>
""", unsafe_allow_html=True)
# Disclaimer
st.markdown("<small>*This is for information purposes only and not considered offical. For further details, please contact the [Federal Programs Team](https://www.sde.idaho.gov/about-us/our-staff/federal-programs/)*</small>", unsafe_allow_html=True)

def get_guidance(grant, expense_type):
    
    df = pd.read_csv("allowable_use_mapping.csv").fillna("")

    # Return all rows if School Improvement or V-B selected
    if grant in ['Title I-A SI','Title V-B']:
        result = df[df['Grant'] == grant][['Guidance','Status']]
        if result.empty:
            return "I didn't quite catch that, please try again or rephrase your request"
        return '\n'.join(result.apply(lambda row: f"{row['Guidance']}: {row['Status']}", axis=1))

    # Return for cases where the expense applies to all grants
    all_match = df[(df['Grant'] == 'All') & (df['Expense Type'].isin(expense_type))]

    grant_match = df[(df['Grant'] == grant) & (df['Expense Type'].isin(expense_type))]

    result = pd.concat([all_match, grant_match])

    if not result.empty:
        return "\n\n".join(result.apply(
            lambda row: f"{row['Expense Type']}-- {row['Guidance']}: {row['Status']}" if row['Guidance'] else f"{row['Expense Type']}-- {row['Status']}",
            axis=1
        ).tolist())

    return "I didn't quite catch that, please try again or rephrase your request"


# Load pre-computed embeddings
with open('embeddings.json', 'r') as f:
    data = json.load(f)

expense_types = data['expense_types']
embeddings = torch.tensor(data['embeddings'])

# Load model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def match_expense(user_input):
    # Account for inappropriate responses because people are terrible
    if profanity.contains_profanity(user_input):
        return []
    
    if any(word in user_input.lower() for word in custom_words):
        return []
    
    # Encode user input
    user_embedding = model.encode(user_input)
    
    # Calculate similarities
    similarities = util.cos_sim(user_embedding, embeddings)[0]
    
    # Get top match
    ranked_idx = similarities.argsort(descending=True)[:10]
    return [expense_types[i] for i in ranked_idx]

# User input


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
        print("Result:", result)  # Debug line
        st.markdown(result)

st.markdown("<small>*This tool can make mistakes</small>", unsafe_allow_html=True)
