import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_job_description(url, driver):
    """
    Scrapes a Workday job posting URL for its job description.
    Uses Selenium as Workday pages are often dynamically loaded.
    """
      # Make sure you have the Chrome driver installed and in your PATH
    job_description = ""
    company_name = ""
    position =  ""
    job_id = ""
    try:
        driver.get(url)
        
        # Wait for the job description div to be present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[3]/div/div/div/div[1]/div[2]/div[2]/div"))
        )
        
        # Extract the job description
        job_description_element = driver.find_element(By.XPATH, "/html/body/div/div/div/div[3]/div/div/div/div[1]/div[2]/div[2]/div")
        job_description = job_description_element.text

        company_name = url.split('.')[0].split('//')[1]

        position_element = driver.find_element(By.XPATH, "/html/body/div/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/h2")
        position = position_element.text

        job_id = url.split('_')[-1]

        
        print(f"✅ Successfully scraped job description from: {url}")
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")

    return company_name, position, job_id, job_description

def get_urls_from_file(file_path):
    """
    Reads URLs from a text file, one URL per line.
    """
    urls = []
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Error: The file {file_path} was not found.")
    return urls

def scrape_all_jobs(file_path='job_links.txt'):
    """
    Main function to read URLs and scrape job descriptions.
    Returns a dictionary of URLs and their corresponding job descriptions.
    """
    driver = webdriver.Chrome()
    job_descriptions = {}
    urls = get_urls_from_file(file_path)
    if not urls:
        print("No URLs found to scrape.")
        return job_descriptions

    for url in urls:
        company_name, position, job_id, description = scrape_job_description(url, driver)
        if description:
            job_descriptions[url] = {
                "Company": company_name,
                "Position": position,
                "Job_ID": job_id,
                "Job_Description": description
            }
    driver.quit()
    return job_descriptions

# Example Usage:
# all_job_descriptions = scrape_all_jobs()
# print(all_job_descriptions)