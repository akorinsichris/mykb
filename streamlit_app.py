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

st.dataframe(existing_data)
