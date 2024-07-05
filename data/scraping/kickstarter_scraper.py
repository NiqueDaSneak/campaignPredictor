import sys
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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

        # Additional content scraping (e.g., story)
        story_content = driver.find_element(By.CSS_SELECTOR, 'div.story-content').text

        project_data = {
            'url': url,
            'goal_amount': float(goal.replace('$', '').replace(',', '')) if goal else 0.0,
            'pledged_amount': float(pledged.replace('$', '').replace(',', '')),
            'backers': int(backers.replace(',', '')),
            'story_content': story_content  # Add this line
        }
    except NoSuchElementException as e:
        print(f"Error scraping URL {url}: {e}", file=sys.stderr)
        project_data = None
    
    driver.quit()
    return project_data

def load_urls(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    urls = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2:
            urls.append((parts[0], parts[1].lower() == 'true'))
        else:
            urls.append((parts[0], False))
    return urls

def save_urls(file_path, urls):
    with open(file_path, 'w') as f:
        for url, processed in urls:
            f.write(f"{url} {processed}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python kickstarter_scraper.py <urls_file>")
        sys.exit(1)
    
    urls_file = sys.argv[1]
    urls = load_urls(urls_file)
    updated_urls = []

    # Ensure the directory for scraped data exists
    if not os.path.exists("data/scraped_data"):
        os.makedirs("data/scraped_data")

    for url, processed in urls:
        if processed:
            updated_urls.append((url, processed))
            continue

        print(f"Scraping data for URL: {url}")
        project_data = scrape_kickstarter(url)
        
        if project_data:
            # Save to JSON file
            file_name = f"scraped_data_{url.replace('https://', '').replace('/', '_')}.json"
            with open(f"data/scraped_data/{file_name}", 'w') as f:
                json.dump(project_data, f)
            
            # Print data to confirm it
            print(json.dumps(project_data, indent=4))
            
            updated_urls.append((url, True))
        else:
            updated_urls.append((url, False))

    save_urls(urls_file, updated_urls)
