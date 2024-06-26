import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
from data.database import insert_raw_data, SessionLocal

def scrape_kickstarter(url):
    options = Options()
    options.headless = True  # Run headless Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    # Extracting pledged amount
    pledged = driver.find_element(By.CSS_SELECTOR, 'span.ksr-green-500').text
    
    # Extract all elements with class 'money' and print their text
    goal_elements = driver.find_elements(By.CSS_SELECTOR, 'span.money')
    
    # Select the correct element with the goal amount (assuming it's the second element)
    goal = goal_elements[1].text if len(goal_elements) > 1 else ""
    
    # Extracting backers
    backers = driver.find_element(By.XPATH, "//div[contains(@class, 'grid-col-12')]/div[contains(@class, 'flex-column-lg')]/div[2]/div/span").text
    
    # Debug prints
    print(f"Pledged: {pledged}")
    print(f"Goal: {goal}")
    print(f"Backers: {backers}")
    
    project_data = {
        'url': url,
        'goal_amount': float(goal.replace('$', '').replace(',', '')) if goal else 0.0,
        'pledged_amount': float(pledged.replace('$', '').replace(',', '')),
        'backers': int(backers.replace(',', ''))
    }
    
    driver.quit()
    return project_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python kickstarter_scraper.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    project_data = scrape_kickstarter(url)
    print(json.dumps(project_data, indent=4))

    # Insert the scraped data into the database
    session = SessionLocal()
    try:
        insert_raw_data(session, project_data)
    finally:
        session.close()
