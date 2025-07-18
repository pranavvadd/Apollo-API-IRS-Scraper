import streamlit as st
from api import run_api_mode  # only import the API mode

def app():
    st.set_page_config(page_title="People Search", page_icon="🔍", layout="wide")
    st.title("Apollo People Search 🔍")

    # No mode selection — just run API mode
    run_api_mode()

if __name__ == "__main__":
    app()
