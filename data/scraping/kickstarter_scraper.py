import sys
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from data.s3_utils import upload_file_to_s3
from selenium.common.exceptions import NoSuchElementException

def scrape_kickstarter(url):
    options = Options()
    options.headless = True  # Run headless Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    try:
        # Extracting pledged amount
        pledged = driver.find_element(By.CSS_SELECTOR, 'span.ksr-green-500').text
        
        # Extract all elements with class 'money' and print their text
        goal_elements = driver.find_elements(By.CSS_SELECTOR, 'span.money')
        
        # Select the correct element with the goal amount (assuming it's the second element)
        goal = goal_elements[1].text if len(goal_elements) > 1 else ""
        
        # Extracting backers
        backers = driver.find_element(By.XPATH, "//div[contains(@class, 'grid-col-12')]/div[contains(@class, 'flex-column-lg')]/div[2]/div/span").text
        
        project_data = {
            'url': url,
            'goal_amount': float(goal.replace('$', '').replace(',', '')) if goal else 0.0,
            'pledged_amount': float(pledged.replace('$', '').replace(',', '')),
            'backers': int(backers.replace(',', ''))
        }
    except NoSuchElementException as e:
        print(f"Error scraping URL {url}: {e}")
        project_data = None
    
    driver.quit()
    return project_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python kickstarter_scraper.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    project_data = scrape_kickstarter(url)
    
    if project_data:
        # Save to JSON file
        with open('scraped_data.json', 'w') as f:
            json.dump([project_data], f)
        
        # Print data to confirm it
        print(json.dumps(project_data, indent=4))
        
        # Upload to S3
        upload_file_to_s3('scraped_data.json', 'bucket-for-crowd-ai')
