
import streamlit as st

# Create a list to store the uploaded file names
file_list = []
st.title("SDE-Assignment 1")
st.markdown("Peer 1")
col1,col2 = st.columns(2)
# Use the file_uploader to allow users to upload files
uploaded_files = col2.file_uploader("Add Files to Network", accept_multiple_files=True)

# Loop through the uploaded files
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        # Append the name of the uploaded file to the file_list
        file_list.append(uploaded_file.name)

# Display the list of uploaded file names
col2.write("Uploaded Files:")
for file_name in file_list:
    # Provide a checkbox for each file name to allow users to remove files
    remove_file = col2.checkbox(file_name)
    if remove_file:
        # Remove the file name from the file_list if the checkbox is selected
        file_list.remove(file_name)
col1.text_input("IP Address")
col1.text_input("Port")
col1.text_input("File hash")
col1.button("Submit")
# Save or load the file_list as needed
# ...
