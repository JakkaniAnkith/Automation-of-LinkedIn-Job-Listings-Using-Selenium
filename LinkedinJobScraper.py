from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os


def scrape_jobs(page_number=2, profession='Data Scientist', location='United States'):
    if ' ' in profession:
        profession = profession.replace(' ', '%20')
    if ' ' in location:
        location = location.replace(' ', '%20')

    driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH
    position_names = []
    companies = []
    locations = []

    path = f'https://www.linkedin.com/jobs/search?keywords={profession}&location={location}'
    driver.get(path)

    i = 0
    while i < page_number:
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        i += 1
        try:
            show_more_button = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[2]/button')
            show_more_button.click()
            time.sleep(2)
        except:
            pass
            time.sleep(3)

    job_list = driver.find_elements(By.CLASS_NAME, 'base-card')
    for job in job_list:
        try:
            position_name = job.find_element(By.TAG_NAME, 'span').text
            position_names.append(position_name)
        except:
            position_names.append(None)

        try:
            company = job.find_element(By.CLASS_NAME, 'hidden-nested-link').text
            companies.append(company)
        except:
            companies.append(None)

        try:
            job_location = job.find_element(By.CLASS_NAME, 'job-search-card__location').text
            locations.append(job_location)
        except:
            locations.append(None)

    data = pd.DataFrame({
        'Position': position_names,
        'Company': companies,
        'Location': locations
    })

    driver.quit()
    return data


def save_jobs_to_csv(data, filename='jobs.csv'):
    # Get the user's home directory
    home_directory = os.path.expanduser("~")

    # Define the full path for the CSV file
    file_path = os.path.join(home_directory, filename)

    # Save the DataFrame to the CSV file
    data.to_csv(file_path, index=False)

    print(f"CSV file has been saved to: {file_path}")


# Example usage
job_data = scrape_jobs(page_number=2, profession='Data Scientist', location='United States')
save_jobs_to_csv(job_data)
