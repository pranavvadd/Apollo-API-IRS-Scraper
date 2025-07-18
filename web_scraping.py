import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def split_name(name):
    if "," in name:
        parts = name.split(",", 1)
        last = parts[0].strip()
        first = parts[1].strip()
    else:
        words = name.split()
        first = words[0] if len(words) > 0 else ""
        last = words[1] if len(words) > 1 else ""
    return first, last

def scrape_irs_data(zip_code, distance, num_pages, include_options):
    driver = webdriver.Chrome()  # make sure chromedriver is installed and on PATH
    driver.get("https://irs.treasury.gov/rpo/rpo.jsf")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "form:country")))
    Select(driver.find_element(By.ID, "form:country")).select_by_visible_text("United States")

    zip_input = driver.find_element(By.ID, "form:address")
    zip_input.clear()
    zip_input.send_keys(zip_code)
    time.sleep(2)

    distance_select = Select(driver.find_element(By.ID, "form:miles"))
    distance_select.select_by_value(str(distance))
    time.sleep(2)

    checkbox_options = {
        "form:attorney": include_options.get("Attorney Credentials", False),
        "form:accountant": include_options.get("CPA Credentials", False),
        "form:agent": include_options.get("Enrolled Agent Credentials", False),
        "form:actuary": include_options.get("Enrolled Actuary Credentials", False),
        "form:retirement": include_options.get("Retirement Plan Agent Credentials", False),
        "form:filingSeasonProgram": include_options.get("Annual Filing Season Credentials", False),
    }

    for box_id, include in checkbox_options.items():
        if include:
            checkbox = driver.find_element(By.ID, box_id)
            if not checkbox.is_selected():
                checkbox.click()

    search_button = driver.find_element(By.ID, "form:search")
    search_button.click()

    data_list = []
    rows = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#form\\:data tbody tr"))
    )

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        data_list.append([col.text.strip() for col in cols])

    for _ in range(num_pages - 1):
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Next >>>']"))
        )
        if next_button.is_enabled():
            next_button.click()
        WebDriverWait(driver, 10).until(EC.staleness_of(rows[0]))
        rows = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#form\\:data tbody tr"))
        )
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            data_list.append([col.text.strip() for col in cols])

    df_full = pd.DataFrame(data_list, columns=["Name", "Credential", "Location", "Distance"])
    df_contacts = pd.DataFrame()
    df_contacts[["First Name", "Last Name"]] = df_full["Name"].apply(lambda n: pd.Series(split_name(n)))
    df_contacts["Phone"] = ""
    df_contacts["Email"] = ""
    df_contacts["Other Info"] = df_full.apply(
        lambda row: f"Credential: {row['Credential']} | Location: {row['Location']} | Distance: {row['Distance']}",
        axis=1
    )

    output_file = "irs_contacts.csv"
    df_contacts.to_csv(output_file, index=False)
    driver.quit()
    return output_file

def main():
    print("Starting IRS Web Scraper (local only)")
    zip_code = input("Enter ZIP code: ").strip()
    distance = input("Enter distance in miles (5, 10, 25, 50, 100, 250): ").strip()
    while distance not in ["5", "10", "25", "50", "100", "250"]:
        print("Invalid distance. Try again.")
        distance = input("Enter distance in miles (5, 10, 25, 50, 100, 250): ").strip()
    distance = int(distance)

    num_pages = input("Enter number of pages to scrape (e.g., 1): ").strip()
    while not num_pages.isdigit() or int(num_pages) < 1:
        print("Please enter a positive integer for pages.")
        num_pages = input("Enter number of pages to scrape (e.g., 1): ").strip()
    num_pages = int(num_pages)

    print("Include credentials (yes/no):")
    include_options = {}
    for credential in [
        "Attorney Credentials",
        "CPA Credentials",
        "Enrolled Agent Credentials",
        "Enrolled Actuary Credentials",
        "Retirement Plan Agent Credentials",
        "Annual Filing Season Credentials"
    ]:
        resp = input(f"Include {credential}? (yes/no): ").strip().lower()
        include_options[credential] = resp == "yes"

    print("Scraping IRS data... this may take a few minutes.")
    output_file = scrape_irs_data(zip_code, distance, num_pages, include_options)
    print(f"Scraping complete. Data saved to {output_file}")

if __name__ == "__main__":
    main()