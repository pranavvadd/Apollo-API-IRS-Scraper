import requests
import pandas as pd
import platform
import os
import json

API_KEY = ""  # Insert your Apollo API key here

# Opens the CSV file after saving, compatible with macOS, Windows, and Linux
def open_file(file_path):
    print(f"Opening file: {file_path}")  # Debug statement
    if platform.system() == "Darwin":
        os.system(f"open {file_path}")
    elif platform.system() == "Windows":
        os.system(f"start {file_path}")
    elif platform.system() == "Linux":
        os.system(f"xdg-open {file_path}")
    else:
        print(f"Please manually open the file located at {file_path}")

# Tries to extract a phone number from either the account or contact-level fields
def get_phone(contact):
    account_phone = contact.get("account", {}).get("phone")
    if account_phone:
        return account_phone
    phone_numbers = contact.get("phone_numbers", [])
    if phone_numbers:
        return phone_numbers[0]
    return "N/A"

# Main function to query the Apollo API and save contacts to a CSV
def search_contacts():
    url = "https://api.apollo.io/api/v1/contacts/search"
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    data = {
        "page": 1,
        "per_page": 10  # Number of results per page
    }

    print("Sending API request with data:")  # Debug
    print(json.dumps(data, indent=2))        # Debug

    response = requests.post(url, headers=headers, json=data)

    print(f"Status code: {response.status_code}")  # Debug
    if response.status_code != 200:
        print(f"API request failed: {response.text}")  # Debug
        return

    results = response.json()
    print("Full response JSON:")  # Debug
    print(json.dumps(results, indent=2))  # Debug

    contacts = results.get("contacts", [])
    print(f"Number of contacts found: {len(contacts)}")  # Debug
    if len(contacts) > 0:
        print("Sample contact data (first 2):", contacts[:2])  # Debug
    else:
        print("No contacts found. Try changing or removing query filters.")

    # Extract relevant fields from each contact
    cleaned = []
    for contact in contacts:
        cleaned.append({
            "First Name": contact.get("first_name"),
            "Last Name": contact.get("last_name"),
            "Email": contact.get("email"),
            "Phone": get_phone(contact)
        })

    if not cleaned:
        print("No contact data to save.")
        return

    # Save contacts to a CSV file
    df = pd.DataFrame(cleaned)
    csv_path = "contacts.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved contacts to {csv_path}")  # Debug

    open_file(csv_path)

if __name__ == "__main__":
    search_contacts()