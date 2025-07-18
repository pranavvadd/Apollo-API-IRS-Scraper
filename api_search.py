import requests

def get_phone(person: dict) -> str:
    phones = person.get("phone_numbers")
    return phones[0] if isinstance(phones, list) and phones else "N/A"

def search_people(api_key, pages, per_page, person_locations=None, jobs=None, domains=None):
    url = "https://api.apollo.io/api/v1/mixed_people/search"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    all_people = []
    for page in range(1, pages + 1):
        payload = {
            "page": page,
            "per_page": per_page,
            **({"person_locations": person_locations} if person_locations else {}),
            **({"person_titles": jobs} if jobs else {}),
            **({"q_organization_domains_list": domains} if domains else {}),
        }

        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
            raise RuntimeError(f"Apollo error {resp.status_code}: {resp.text}")

        data = resp.json()
        if "error" in data:
            raise RuntimeError(f"Apollo API error: {data['error']}")

        people = data.get("people", [])
        if not people:
            break
        all_people.extend(people)

    return all_people

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