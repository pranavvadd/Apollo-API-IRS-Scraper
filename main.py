import requests

def get_phone(person: dict) -> str:
    return (person.get("phone_numbers") or ["N/A"])[0]

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

        people = resp.json().get("people", [])
        if not people:
            break
        all_people.extend(people)

    return all_people

def clean_people_data(all_people):
    return [{
        "First Name": p.get("first_name"),
        "Last Name": p.get("last_name"),
        "Email": p.get("email"),
        "Phone": get_phone(p),
        "Title": p.get("title"),
        "Company": p.get("organization_name"),
        "Location": ", ".join(filter(None, [p.get("city"), p.get("state")])),
        "LinkedIn": p.get("linkedin_url")
    } for p in all_people]