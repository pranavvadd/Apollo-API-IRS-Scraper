# IRS Scraper — Version 2 using Apollo.io's API

An interactive Python web app that uses the Apollo API to programmatically retrieve contact information for IRS-credentialed tax professionals. This tool allows users to enter search filters (such as city, state, job title, and company domain), fetch results using the Apollo API, and export the cleaned contact data into a CSV file.

---

## What Version 2 Does

- Sends POST requests to the Apollo API’s people search endpoint with pagination and filter support.
- Extracts contact information: First Name, Last Name, Email, Phone, Company, Title, and LinkedIn.
- Displays results in an interactive UI built with Streamlit.
- Allows users to download search results as a CSV file.

---

## Development Journey

The project began with a Selenium-based IRS RPO directory scraper. However, due to the complexity of extracting emails and phone numbers from the site, the project pivoted to the Apollo API.

Using the Apollo API allowed structured data access and cleaner logic, though it introduced limitations in the volume and types of accessible data due to API plan restrictions. To make the experience user-friendly and accessible, the project was transitioned into a web app with a clean UI using Streamlit.

---

## Technical Features

- Modular code split between a backend (`main.py`) and a UI (`ui.py`).
- API key management:
  - Users can manually enter their Apollo API key once through the UI.
  - The key is stored securely in `st.session_state` for the duration of the session.
- Error handling for invalid keys or failed requests.
- Search filters include:
  - City and State
  - Job Titles (comma-separated)
  - Company Domains (comma-separated)
  - Number of Pages and People per Page

---

## Deployment Plan

This project will be deployed publicly using **Streamlit Community Cloud**, making it accessible to any user with an Apollo API key. Users will:

1. Visit the hosted app link.
2. Enter their API key directly into the interface.
3. Enter search filters.
4. View, filter, and download results.

This approach removes the need for manual setup or local execution, enabling broader and easier access.

---

## Tech Stack

- **Language**: Python 3.11  
- **Libraries**: `requests`, `pandas`, `streamlit`  
- **API**: Apollo People Search API  
- **UI**: Streamlit Web App  

---

## Limitations

- Apollo API access is subject to your API plan (must be paid otherwise no data will be retrieved).
- Some searches may return limited or no results depending on your query filters and API rate limits.

---

## Future Plans

- Have an option for the user to interact with a "free scraper" (one that doesn't need a paid API key), I can use my Selenium version for that
- Add caching to reduce repeated API calls.
- Support for saving session history.
- Basic data visualizations (location heatmap, job title distribution).
- Pagination controls in UI to load results dynamically.

---

## Getting Started Locally

To run the project on your local machine:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/IRS-Scraper-Version-2.git
cd IRS-Scraper-Version-2

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run ui.py
