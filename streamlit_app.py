import streamlit as st
import requests

st.title("🏥 Pain & Go Hospital Assistant")
st.caption("Ask about doctors, services, or hospital policies")

query = st.text_input("Your question:")
if query:
    response = requests.post("http://localhost:8000/ask", json={"query": query})
    if response.status_code == 200:
        st.success(response.json()["response"])
    else:
        st.error("Error processing request")