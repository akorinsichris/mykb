import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Desription
st.title("My Knowledge Base Portal":open_book:)
st.markdown("Enter the details of the new knowledge information below.")

# Establishing a Google Sheets Connection
conn = st.experimental_connection('gsheets', type=GSheetsConnection)

#Fetch exist data
existing_data = conn.read(worksheet="knowledgebase", usecols=list(range(3)), ttl=5)
existing_data = existing_data.dropna(how="all")

# st.dataframe(existing_data)

CATEGORY = [
  "Linux",
  "Network",
  "PostgreSQL",
  "Python",
  "Snowflake",
  "Technology",
  "Teradata",
]

# Onboarding New KB Form
with st.form(key="kb_form"):
    cols = st.columns((1, 1))
    category_name = cols[0].selectbox("Category*:", options=CATEGORY )
    subject_name = cols[1].text_input(label="Subject*:")
    description = st.text_area(label="Description")
    

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit KB Details")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not category_name or not subject_name:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        elif existing_data["Subject"].str.contains(subject_name).any():
            st.warning("A subject like this name already exists.")
            st.stop()
        else:
            # Create a new row of kb data
            kb_data = pd.DataFrame(
                [
                    {
                        "Category": category_name,
                        "Subject": subject_name,
                        "Description": description,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, kb_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="knowledgebase", data=updated_df)

            st.success("KnowledgeBase details successfully addedd!")
