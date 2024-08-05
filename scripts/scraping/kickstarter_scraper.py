import sys
import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def scrape_kickstarter(url):
    options = Options()
    options.headless = True  # Run headless Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    def extract_data():
        try:
            # Try primary selectors first
            pledged_element = driver.find_element(By.CSS_SELECTOR, 'div.col-right.col-4.py3.border-left.spotlight-project-video-archive > div.mb3 > h3.mb0 > span.money')
            pledged = pledged_element.text.replace('$', '').replace(',', '').strip()

            goal_element = driver.find_element(By.CSS_SELECTOR, 'div.type-12.medium.navy-500 > span.money')
            goal = goal_element.text.replace('$', '').replace(',', '').strip()
            
            backers_element = driver.find_element(By.CSS_SELECTOR, 'div.mb0 > h3.mb0')
            backers = backers_element.text.replace(',', '').strip()

            story_content_element = driver.find_element(By.CSS_SELECTOR, 'div.story-content')
            story_content = story_content_element.text.strip()

            return {
                'url': url,
                'goal_amount': float(goal) if goal else None,
                'pledged_amount': float(pledged) if pledged else None,
                'backers': int(backers) if backers else None,
                'story_content': story_content
            }
        except NoSuchElementException:
            try:
                # Try alternative selectors
                pledged_element = driver.find_element(By.CSS_SELECTOR, 'div.grid-col-12.grid-col-4-md.hide.block-lg span.ksr-green-500')
                pledged = pledged_element.text.replace('$', '').replace(',', '').strip()

                goal_element = driver.find_element(By.CSS_SELECTOR, 'div.grid-col-12.grid-col-4-md.hide.block-lg span.money')
                goal = goal_element.text.replace('$', '').replace(',', '').strip()
                
                backers_element = driver.find_element(By.CSS_SELECTOR, 'div.grid-col-12.grid-col-4-md.hide.block-lg div.type-16.type-28-md.bold.dark-grey-500 > span')
                backers = backers_element.text.replace(',', '').strip()

                story_content_element = driver.find_element(By.CSS_SELECTOR, 'div.story-content')
                story_content = story_content_element.text.strip()

                return {
                    'url': url,
                    'goal_amount': float(goal) if goal else None,
                    'pledged_amount': float(pledged) if pledged else None,
                    'backers': int(backers) if backers else None,
                    'story_content': story_content
                }
            except NoSuchElementException as e:
                print(f"Error scraping URL {url} with both primary and fallback selectors: {e}", file=sys.stderr)
                return None

    project_data = extract_data()
    driver.quit()
    return project_data

def load_urls(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    urls = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 3:
            urls.append((parts[0], parts[1].lower() == 'true', parts[2].lower() == 'true'))
        else:
            urls.append((parts[0], False, False))
    return urls

def save_urls(file_path, urls):
    with open(file_path, 'w') as f:
        for url, scraped, uploaded in urls:
            f.write(f"{url} {scraped} {uploaded}\n")

def save_to_csv(data, file_path):
    df = pd.DataFrame([data])
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    urls_file = 'urls.txt'
    urls = load_urls(urls_file)
    updated_urls = []

    # Ensure the directory for scraped data exists
    if not os.path.exists("../../data/scraped_data"):
        os.makedirs("../../data/scraped_data")

    for url, scraped, uploaded in urls:
        if scraped:
            updated_urls.append((url, scraped, uploaded))
            continue

        print(f"Scraping data for URL: {url}")
        project_data = scrape_kickstarter(url)
        
        if project_data:
            # Save to JSON file
            json_file_name = f"scraped_data_{url.replace('https://', '').replace('/', '_')}.json"
            with open(f"../../data/scraped_data/{json_file_name}", 'w') as f:
                json.dump(project_data, f)
            
            # Save to CSV file
            csv_file_name = f"scraped_data_{url.replace('https://', '').replace('/', '_')}.csv"
            save_to_csv(project_data, f"../../data/scraped_data/{csv_file_name}")
            
            # Print data to confirm it
            print(json.dumps(project_data, indent=4))
            
            updated_urls.append((url, True, uploaded))
        else:
            updated_urls.append((url, scraped, uploaded))

    save_urls(urls_file, updated_urls)