import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Desription
st.title("My Knowledge Base Portal")
st.markdown("Enter the details of the new knowledge information below.")

# Establishing a Google Sheets Connection
conn = st.experimental_connection('gsheets', type=GSheetsConnection)

#Fetch exist data
existing_data = conn.read(worksheet="knowledgebase", usecols=list(range(4)), ttl=5)
existing_data = existing_data.dropna(how="all")

# st.dataframe(existing_data)

CATEGORY = [
  "Linux",
  "Technology",
  "Snowflake",
  "PostgreSQL",
  "Teradata",
]

# onboarding a new kb form
with st.form(key="kb_form"):
  category_name = st.selectbox("Category*", options=CATEGORY)
  subject = st.text_input(label="Subject*")
  description = st.text_area(label="Description")

# Mark mandatory fields
st.markdown("**required*")

submit_button = st.form_submit_button(lable="Submit")

# if submit button is pressed
if submit_button:
  st.write("submit was pressed")
  
  
