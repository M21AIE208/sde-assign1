
import streamlit as st
from node import Node

#initialising the node from Node class
node = Node("0.0.0.0",5001)

file_list = []
st.title("SDE-Assignment 1")
st.markdown("Peer 1")
col1,col2 = st.columns(2)


uploader = col2.file_uploader("Add Files to Network", accept_multiple_files=True)

for uploaded_file in uploader:
    if uploaded_file is not None:        
        hash = node.add_file(f"/home/ajay/Downloads/{uploaded_file.name}") #change this location as per OS 
        col2.write(hash)
        file_list.append(uploaded_file.name)


col2.write("Uploaded Files:")
for file_name in file_list:
    remove_file = col2.checkbox(file_name)
    if remove_file:
        file_list.remove(file_name)

#reading input from the user
ip = col1.text_input("IP Address")
port = col1.text_input("Port")
filehash = col1.text_input("File hash")


#callback funcitonality
if col1.button("Request File"):
	node.request_file()

if col2.button("Accept File"):
    try:
        node.send_file(filehash,str(ip),int(port))
        col2.success("File Downloaded")
    except:
        col2.warning("Error Downloading File")

