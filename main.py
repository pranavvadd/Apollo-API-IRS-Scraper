import requests
import pandas as pd
import platform
import os
import json

API_KEY = "OMPiK679F6Yf10sgbw56WA"  # Your API key here

def open_file(file_path):
    if platform.system() == "Darwin":
        os.system(f"open {file_path}")
    elif platform.system() == "Windows":
        os.system(f"start {file_path}")
    elif platform.system() == "Linux":
        os.system(f"xdg-open {file_path}")
    else:
        print(f"Please open the file manually: {file_path}")

def get_phone(contact):
    account_phone = contact.get("account", {}).get("phone")
    if account_phone:
        return account_phone
    phone_numbers = contact.get("phone_numbers", [])
    if phone_numbers:
        return phone_numbers[0]
    return "N/A"

def search_contacts():
    pages = int(input("Enter the number of pages to retrieve: "))
    per_page = int(input("Enter the number of contacts per page (max 100): "))
    city = input("Enter city (or leave blank for any): ").strip()
    state = input("Enter state (or leave blank for any): ").strip()

    location_keywords = []
    if city and state:
        location_keywords.append(f"{city}, {state}")
    elif city:
        location_keywords.append(city)
    elif state:
        location_keywords.append(state)

    job_title_input = input("Enter job titles (comma-separated) or leave blank: ").strip()
    jobs = [job.strip() for job in job_title_input.split(",")] if job_title_input else []

    company_input = input("Enter company domains (comma-separated) or leave blank: ").strip()
    domains = [domain.strip() for domain in company_input.split(",")] if company_input else []

    url = "https://api.apollo.io/api/v1/contacts/search"
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    all_contacts = []

    for page in range(1, pages + 1):
        print(f"\nProcessing page {page} of {pages}...")
        data = {
            "page": page,
            "per_page": per_page,
            "location_keywords": location_keywords,
            "title_keywords": jobs,
            "q_organization_domains": domains
        }

        print("Sending API request with data:")
        print(json.dumps(data, indent=2))

        response = requests.post(url, headers=headers, json=data)

        print(f"Status code: {response.status_code}")
        if response.status_code != 200:
            print(f"API request failed: {response.text}")
            return

        results = response.json()
        contacts = results.get("contacts", [])

        if not contacts:
            print("No contacts found on this page.")
            break

        print(f"Found {len(contacts)} contacts on page {page}.")
        print("Sample contact (first one):")
        print(json.dumps(contacts[0], indent=2))

        all_contacts.extend(contacts)

    if not all_contacts:
        print("No contacts to save.")
        return

    cleaned = [{
        "First Name": c.get("first_name"),
        "Last Name": c.get("last_name"),
        "Email": c.get("email"),
        "Phone": get_phone(c),
        "Title": c.get("title"),
        "Company": c.get("organization_name") or c.get("organization", {}).get("name") or c.get("account", {}).get("name"),
        "Location": c.get("present_raw_address") or f"{c.get('city', '')}, {c.get('state', '')}".strip(", ")
    } for c in all_contacts]

    df = pd.DataFrame(cleaned)
    csv_path = "contacts.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nSaved {len(cleaned)} contacts to {csv_path}")
    open_file(csv_path)

if __name__ == "__main__":
    search_contacts()