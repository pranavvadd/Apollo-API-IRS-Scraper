import streamlit as st
from api import run_api_mode
from web_scraping import run_web_scraper_mode

# Set up the Streamlit app with a title and radio buttons for mode selection
def app():
    st.set_page_config(page_title="People Search", page_icon="🔍", layout="wide")
    st.title("People Search 🔍")

    mode = st.radio(
        "Choose search method:",
        ["Use Apollo API (Full Data)", "Use IRS Web Scraper (No Emails/Phones)"]
    )

    if mode == "Use Apollo API (Full Data)":
        run_api_mode() # Run the API mode function
    else:
        run_web_scraper_mode() # Run the web scraper mode function

if __name__ == "__main__":
    app()