import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

def split_name(name):
    if "," in name:
        parts = name.split(",", 1)
        last = parts[0].strip()
        first = parts[1].strip()
    else:
        words = name.split()
        first = words[0] if len(words) > 0 else ""
        last = words[1] if len(words) > 1 else ""
    return pd.Series([first, last])

def scrape_irs_data(zip_code, distance, num_pages, include_options):
    driver = webdriver.Chrome()
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
        "form:attorney": include_options["Attorney Credentials"],
        "form:accountant": include_options["CPA Credentials"],
        "form:agent": include_options["Enrolled Agent Credentials"],
        "form:actuary": include_options["Enrolled Actuary Credentials"],
        "form:retirement": include_options["Retirement Plan Agent Credentials"],
        "form:filingSeasonProgram": include_options["Annual Filing Season Credentials"]
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
    df_contacts[["First Name", "Last Name"]] = df_full["Name"].apply(split_name)
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

def run_web_scraper_mode():
    st.header("IRS Web Scraper")
    st.warning(
        "⚠ **Disclaimer:** This method does NOT return phone numbers or emails. "
        "Only names and basic details will be provided. "
        "You will need to manually find and reformat contact info."
    )

    with st.form("web_scraper_form"):
        zip_code = st.text_input("ZIP Code")
        num_pages = st.number_input("Number of pages to navigate", min_value=1, max_value=100, value=1)
        distance = st.selectbox("Distance (miles)", [5, 10, 25, 50, 100, 250])

        st.markdown("**Select credentials to include:**")
        include_options = {
            "Attorney Credentials": st.checkbox("Attorney Credentials"),
            "CPA Credentials": st.checkbox("CPA Credentials"),
            "Enrolled Agent Credentials": st.checkbox("Enrolled Agent Credentials"),
            "Enrolled Actuary Credentials": st.checkbox("Enrolled Actuary Credentials"),
            "Retirement Plan Agent Credentials": st.checkbox("Retirement Plan Agent Credentials"),
            "Annual Filing Season Credentials": st.checkbox("Annual Filing Season Credentials"),
        }

        submit_web = st.form_submit_button("Run Web Scraper")

    if submit_web:
        with st.spinner("Scraping IRS data... This may take some time."):
            try:
                output_file = scrape_irs_data(zip_code, distance, num_pages, include_options)
                st.success("Scraping complete.")
                with open(output_file, "rb") as f:
                    st.download_button(
                        "Download CSV",
                        f,
                        file_name="irs_contacts.csv",
                        mime="text/csv"
                    )
            except Exception as e:
                st.error(f"Error during web scraping: {e}")