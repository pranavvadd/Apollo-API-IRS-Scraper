import streamlit as st
import datetime as dt
import pandas as pd
from api_search import search_people, clean_people_data  # your backend API functions

# Run the Streamlit app in API mode with a form for user input
def run_api_mode():
    st.header("Apollo API Search")

    # API Key Input
    if "api_key" not in st.session_state:
        key_from_secrets = st.secrets.get("api_key", "")
        st.session_state.api_key = key_from_secrets or ""

    # Input for API Key
    API_KEY = st.text_input(
        "Apollo API Key",
        type="password",
        value=st.session_state.api_key,
        help="Enter your Apollo API key. It will remain stored during this session."
    )
    st.session_state.api_key = API_KEY

    # Check if API Key is provided
    if not API_KEY:
        st.warning("Please enter your API key to continue.")
        return

    # Search Form
    with st.form("search_form"):
        st.subheader("Search Parameters")
        col1, col2 = st.columns(2)
        with col1:
            pages = st.number_input("Pages", min_value=1, max_value=100, value=1)
            city = st.text_input("City (optional)")
            jobs_input = st.text_input("Job titles (comma-separated, optional)")
        with col2:
            per_page = st.number_input("People per page (max 100)", min_value=1, max_value=100, value=25)
            state = st.text_input("State (optional)")
            domains_input = st.text_input("Company domains (comma-separated, optional)")

        submit = st.form_submit_button("Search")

    # Process the form submission and putting together the search parameters in a list
    if submit:
        person_locations = []
        if city and state:
            person_locations = [f"{city}, {state}"]
        elif city:
            person_locations = [city]
        elif state:
            person_locations = [state]

        # Split and clean job titles and domains inputs
        jobs = [j.strip() for j in jobs_input.split(",") if j.strip()]
        domains = [d.strip() for d in domains_input.split(",") if d.strip()]

        # Validate inputs and call the search function
        with st.spinner("Searching..."):
            try:
                all_people = search_people(
                    api_key=API_KEY,
                    pages=pages,
                    per_page=per_page,
                    person_locations=person_locations,
                    jobs=jobs,
                    domains=domains,
                )
            except Exception as e:
                st.error(f"Error while fetching data: {e}")
                return

        # If no people found, show a warning
        if not all_people:
            st.warning("No people found.")
            return

        # Clean and prepare the data for display
        df_full = pd.DataFrame(clean_people_data(all_people))
        st.subheader(f"Found {len(df_full)} people")

        # Show preview table with all columns (full details)
        max_preview = 200
        st.markdown("### Preview (Full Details)")
        if len(df_full) > max_preview:
            st.dataframe(df_full.head(max_preview))
            st.caption(f"Showing first {max_preview} rows.")
        else:
            st.dataframe(df_full)

        # Show simplified table for manual review (First Name, Last Name, Email, Phone)
        st.markdown("### Simplified Table (Readily Uploadable to CRM)")
        simplified_cols = ["First Name", "Last Name", "Email", "Phone"]
        df_simple = df_full[simplified_cols]
        st.dataframe(df_simple)

        # Download button for simplified CSV only (no extra columns)
        csv_simple = df_simple.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Simplified CSV",
            data=csv_simple,
            file_name=f"people_simplified-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}.csv",
            mime="text/csv",
        )