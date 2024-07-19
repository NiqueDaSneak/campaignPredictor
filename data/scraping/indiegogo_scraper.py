import json
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_indiegogo(url):
    options = Options()
    options.headless = True  # Run headless Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    
    try:
        # Extracting pledged amount
        pledged_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.basicsGoalProgress-amountSold.t-rebrand-h4s')))
        pledged = pledged_element.text.strip()
        
        # Extracting goal amount and percentage
        goal_element = driver.find_element(By.CSS_SELECTOR, 'span.basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOrInitiallyRaised')
        goal_info = goal_element.text.strip()
        goal_amount_parts = goal_info.split('of ')
        if len(goal_amount_parts) > 1:
            goal_amount = goal_amount_parts[1].split(' ')[0].replace('$', '').replace(',', '')
        else:
            goal_amount = '0'  # Default value if the goal amount is not found
        
        # Extracting backers
        backers_element = driver.find_element(By.CSS_SELECTOR, 'span.basicsGoalProgress-claimedOrBackers')
        backers_text = backers_element.text.strip()
        backers = [int(s.replace(',', '')) for s in backers_text.split() if s.replace(',', '').isdigit()][0]

        # Extracting story content
        story_element = driver.find_element(By.CSS_SELECTOR, 'div.routerContentStory-storyBody')
        story_content = story_element.text.strip()

        project_data = {
            'url': url,
            'goal_amount': float(goal_amount),
            'pledged_amount': float(pledged.replace('$', '').replace(',', '')),
            'backers': backers,
            'story_content': story_content
        }
    except (TimeoutException, NoSuchElementException, ValueError, IndexError) as e:
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
        print("Usage: python indiegogo_scraper.py <urls_file>")
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
        project_data = scrape_indiegogo(url)
        
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
