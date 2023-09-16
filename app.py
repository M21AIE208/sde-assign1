
import streamlit as st
from node import Node

node = Node("0.0.0.0",5001)

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
        
        hash = node.add_file(f"/home/ajay/Downloads/{uploaded_file.name}")
        col2.write(hash)
        file_list.append(uploaded_file.name)

# Display the list of uploaded file names
col2.write("Uploaded Files:")
for file_name in file_list:
    # Provide a checkbox for each file name to allow users to remove files
    remove_file = col2.checkbox(file_name)
    if remove_file:
        # Remove the file name from the file_list if the checkbox is selected
        file_list.remove(file_name)
ip = col1.text_input("IP Address")
port = col1.text_input("Port")
filehash = col1.text_input("File hash")



if col1.button("Request File"):
	node.request_file()

if col2.button("Accept File"):
    try:
        node.send_file(filehash,str(ip),int(port))
        col2.success("File Downloaded")
    except:
        col2.warning("Error Downloading File")

