# IRS Scraper Backend — Version 2

An automated Python script that uses the Apollo API to programmatically retrieve contact information for IRS-credentialed tax professionals. The script sends structured API requests, parses JSON responses, and exports cleaned contact data (first name, last name, email, phone) into a CSV file for easy access and analysis.

---

## What Version 2 Is Designed To Do

Version 2 is designed to programmatically retrieve IRS-related contact information via the Apollo API. While the code successfully queries the API and processes responses, available data is limited due to API access restrictions encountered during development.

- Sends POST requests to the Apollo API contacts search endpoint with pagination support.
- Extracts key contact fields: First Name, Last Name, Email, and Phone Number.
- Saves the retrieved contact information into `contacts.csv`.
- Opens the CSV file automatically upon completion for user convenience.

---

## Development Journey and Challenges

Initially, I built a Selenium-based web scraper to collect data directly from the IRS Registered Tax Return Preparers Online (RPO) directory. This allowed dynamic interaction with the website’s search filters and pagination.

However, scraping emails and phone numbers separately from the site proved technically challenging due to the dispersed nature of contact details and complex page navigation.

To address these challenges, I pivoted to using the Apollo API to retrieve structured contact data programmatically. While this simplified data handling, I encountered API access limitations and restrictions that constrained the volume of retrievable data despite extensive testing with varying page numbers and filters.

---

## Technical Debugging and Hurdles

During development, I implemented status code checks to verify successful API responses and added handling for cases where no contacts were returned, ensuring graceful failure and clear messaging.

I experimented with refining query parameters by both narrowing and broadening search categories in an effort to retrieve more comprehensive data. Despite these efforts, the API consistently returned limited or no contact data due to access restrictions.

Recognizing these limitations, I am revisiting the Selenium-based scraper, which has greater potential for accessing foundational contact information directly from the IRS site. Although this API-driven approach is a valuable learning experience, I view this project as ongoing and plan to further develop and integrate both methods in the future.

---

## Next Steps and Future Work

To continue providing valuable data to users, I plan to revisit and refine the Selenium scraper to reliably extract first and last names from the RPO directory. This dataset will serve as a foundation for users to manually supplement missing emails and phone numbers.

Additionally, I intend to develop a lightweight user interface using Flask for the backend and a simple frontend framework. This UI will allow users to interactively search, view, and enrich scraped data in a user-friendly environment.

## Future Enhancements

- I plan to explore enhancing API pagination handling to retrieve larger datasets.
- Future work could include adding robust error handling and retry logic for API rate limits and failures.
- I aim to integrate the Selenium scraper to provide foundational name data where API access is limited.
- The development of a Flask backend connected to a frontend UI (potentially React with JSX or vanilla JS) is a possibility to enable interactive user data exploration and manual augmentation of contact information.
- Expanding data export formats (Excel, JSON) and filtering options may also be added.

---

## Tech Stack

- Language: Python 3.11  
- Libraries: `requests`, `pandas`  
- API: Apollo Contacts Search API  
- (Planned) Backend UI: Flask  
- (Planned) Frontend UI: TBD (could be React with JSX, vanilla JavaScript, or other frameworks)

---

## Getting Started

To set up and run the project:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/IRS-Scraper-Version-2.git
cd IRS-Scraper-Version-2

# 2. Install dependencies
pip install requests pandas

# 3. Insert your Apollo API key
# Open the script and replace the line with your actual API key:
# API_KEY = "YOUR_ACTUAL_API_KEY_HERE"

# 4. Run the script
python main.py
