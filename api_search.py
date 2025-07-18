import requests

# This module provides functions to search for people using the Apollo API.
def get_phone(person: dict) -> str:
    phones = person.get("phone_numbers")
    return phones[0] if isinstance(phones, list) and phones else "N/A"

# Searches for people using the Apollo API.
def search_people(api_key, pages, per_page, person_locations=None, jobs=None, domains=None):
    url = "https://api.apollo.io/api/v1/mixed_people/search"
    
    # Set up headers for the API request
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    # Validate input parameters
    all_people = []
    for page in range(1, pages + 1):
        payload = {
            "page": page,
            "per_page": per_page,
            **({"person_locations": person_locations} if person_locations else {}),
            **({"person_titles": jobs} if jobs else {}),
            **({"q_organization_domains_list": domains} if domains else {}),
        }

        # Make the API request
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
            raise RuntimeError(f"Apollo error {resp.status_code}: {resp.text}")

        # Check for errors in the response
        data = resp.json()
        if "error" in data:
            raise RuntimeError(f"Apollo API error: {data['error']}")

        # Extract people data from the response
        people = data.get("people", [])
        if not people:
            break
        all_people.extend(people)

    return all_people

# Cleans and formats the people data retrieved from the Apollo API.
def clean_people_data(all_people):
    return [{
        "First Name": p.get("first_name", "N/A"),
        "Last Name": p.get("last_name", "N/A"),
        "Email": p.get("email", "N/A"),
        "Phone": get_phone(p),
        "Title": p.get("title", "N/A"),
        "Company": p.get("organization_name", "N/A"),
        "Location": ", ".join(filter(None, [p.get("city"), p.get("state")])),
        "LinkedIn": p.get("linkedin_url", "N/A")
    } for p in all_people]