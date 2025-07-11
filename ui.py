import streamlit as st
import main  # your backend functions
import datetime as dt
import pandas as pd

def app():
    st.title("Apollo People Search 🔍")

    # --- API KEY handling with session state and editable input ---
    if "api_key" not in st.session_state:
        key_from_secrets = st.secrets.get("api_key", "")
        if key_from_secrets:
            st.session_state.api_key = key_from_secrets
        else:
            st.session_state.api_key = ""

    # Show the API key input so user can view or change it anytime
    API_KEY = st.text_input("Apollo API Key", type="password", value=st.session_state.api_key)
    if not API_KEY:
        st.warning("Please enter your API key to continue.")
        st.stop()
    else:
        st.session_state.api_key = API_KEY

    # --- Search Form ---
    with st.form("search_form"):
        st.header("Search Parameters")

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

    # --- Search Submission ---
    if submit:
        person_locations = []
        if city and state:
            person_locations = [f"{city}, {state}"]
        elif city:
            person_locations = [city]
        elif state:
            person_locations = [state]

        jobs = [j.strip() for j in jobs_input.split(",") if j.strip()]
        domains = [d.strip() for d in domains_input.split(",") if d.strip()]

        with st.spinner("Searching..."):
            try:
                all_people = main.search_people(
                    api_key=API_KEY,
                    pages=pages,
                    per_page=per_page,
                    person_locations=person_locations,
                    jobs=jobs,
                    domains=domains,
                )
            except Exception as e:
                st.error(f"Error: {e}")
                return

        if not all_people:
            st.warning("No people found.")
            return

        df = pd.DataFrame(main.clean_people_data(all_people))
        st.subheader(f"Found {len(df)} people")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name=f"people-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    app()