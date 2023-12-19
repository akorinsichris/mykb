import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Desription
st.title("My Knowledge Base Portal")
st.markdown("Enter the details of the new knowledge information below.")

# Establishing a Google Sheets Connection
conn = st.experimental_connection('gsheets', type=GSheetsConnection)

#Fetch exist data
existing_data = conn.read(worksheet="knowledgebase", usecols=list(range(3)), ttl=5)
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
    # check all mandatory field are filled
    if not category_name or not subject:
      st.warning("Ensure all mandatory fields are filled.")
      st.stop()
    elif existing_data["Subject"].str.contains(subject).any():
      st.warning("Subject already exists.")
      st.stop()
    else:
      # create a new row of kb data
      kb_data = pd.DataFrame(
        [
          {
            "Category": category_name,
            "Subject": subject,
            "Description": description,
          }
        ]
      )
    
      # Add the new kb data to the existing data
      updated_df = pd.concat([existing_data, kb_data], ignore_index=True)

      # Update Google Sheets with the new kb data
      conn.update(worksheet="knowledgebase", data=updated_df)
  
      st.write("Records Save")
  
  
