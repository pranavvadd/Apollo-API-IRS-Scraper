# Tax Pro Searcher using Apollo and Selenium

An interactive Python tool for finding IRS-credentialed tax professionals. It offers two components:

1. **Apollo API Web App** — A Streamlit-based web app (deployed online) that uses Apollo.io’s API to fetch detailed contact data, including email and phone numbers.  
2. **IRS Selenium Scraper** — A local script for scraping IRS RPO directory data (names, credentials, and locations) when API access isn’t available.

---

## Elevator Pitch

Finding accurate and complete contact information for tax professionals is time-consuming. **Tax Pro Searcher** automates this process by integrating Apollo.io’s API with a fallback local IRS scraper. Users can easily search, preview, and download clean contact datasets, all through a simple Streamlit interface for API-based searches, or a local Selenium-based scraper for basic data.

---

## Tech Stack

- **Python 3.8+** — Core programming language  
- **Streamlit** — Frontend web app framework for interactive UI  
- **Apollo.io API** — Data source for enriched contact information  
- **Selenium WebDriver** — Web scraping automation for IRS directory  
- **Pandas** — Data processing and CSV export  
- **ChromeDriver** — Browser driver for Selenium automation  
- **Requests** — HTTP requests for API communication  

---

## What It Does

### Apollo Mode

- Sends **JSON POST requests** to Apollo API’s people search endpoint.  
- Fetches details like first/last name, email, phone, title, company, location, and LinkedIn.  
- Displays results interactively in Streamlit with options to preview and download data as CSV.

### IRS Selenium Scraper

- Uses Selenium WebDriver to automate searches on the IRS RPO directory.  
- Extracts names, credentials, and locations.  
- Exports results to a CSV file for manual review and enrichment.

---

## Technical Features
- Apollo API Integration — Queries Apollo.io for structured contact data with filtering.
- Streamlit UI — Provides a responsive and interactive web interface for searches.
- CSV Export Options — Allows downloading of detailed or simplified CSV files.
- Local Selenium Scraper — Automates IRS RPO directory queries when API data isn’t available.
- Secure API Key Handling — Safely stores Apollo API keys within Streamlit session state.
- Flexible Search Filters — Filter results by city, state, job title, company domain, and more.

---

## Development Workflow
### Phase 1
- Built a Selenium-based scraper for the IRS RPO directory.
### Phase 2
- Integrated Apollo.io API to fetch structured contact data including emails and phones.
### Phase 3
- Added a Streamlit user interface for easy access and interaction.
### Phase 4
- Deployed the Apollo app online; retained the IRS scraper as a local, standalone tool.

---

## Limitations
- Apollo API requires a paid key — Without an active key, the API-based search returns no results.
- Rate limits on Apollo API — The number of daily API requests may be limited depending on your subscription.
- IRS scraper lacks email and phone info — It only collects names, credentials, and locations; further manual lookups are necessary.
- Web scraper cannot run in the cloud — Must be executed locally due to browser dependencies.

---

## Future Plans
- Add basic visualizations (e.g., location heatmaps, job title distribution).
- Enable session history and local caching of results.
- Offer CRM integration with tools like Salesforce or HubSpot.
- Introduce a free scraping mode with open-source alternatives.

---

## Running the IRS Web Scraper Locally

1. Clone the repository  
    ```bash
    git clone https://github.com/pranavvadd/Tax-Pro-Searcher.git
    cd Tax-Pro-Searcher
    ```

2. Install dependencies  
    ```bash
    pip install -r requirements.txt
    ```

3. Run the local scraper  
    ```bash
    python web_scraping.py
    ```

---

## Running the Apollo API Web App

1. Clone the repository (if not already done)  
    ```bash
    git clone https://github.com/pranavvadd/Tax-Pro-Searcher.git
    cd Tax-Pro-Searcher
    ```

2. Install dependencies  
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app  
    ```bash
    streamlit run app.py
    ```

---

## Access the Deployed Apollo App

Use this link to access the online version of the Apollo API web app:  
[https://taxprofinder.streamlit.app/](https://taxprofinder.streamlit.app/)

---

## Architecture

```plaintext
+------------------------+
|  Streamlit Web App     |  (Deployed on Streamlit Cloud)
|  - app.py              |
|  - api.py              |
|  - api_search.py       |
+------------------------+
            |
            v
    Apollo.io API (Cloud)

(Local, Separate Component)
+------------------------+
|  IRS Web Scraper       |
|  - web_scraping.py     |
|  (Runs locally)        |
+------------------------+
