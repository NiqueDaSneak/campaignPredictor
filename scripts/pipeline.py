import sys
import os
import pandas as pd
import json

from data.s3_utils import upload_file_to_s3, download_file_from_s3
from data.preprocessing.preprocessing import preprocess_data
from data.scraping.kickstarter_scraper import scrape_kickstarter

BUCKET_NAME = "bucket-for-crowd-ai"

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

def check_if_data_exists(url):
    file_name = f"scraped_data_{url.replace('https://', '').replace('/', '_')}.json"
    try:
        download_file_from_s3(BUCKET_NAME, file_name)
        return True
    except Exception as e:
        return False

def main(urls_file):
    urls = load_urls(urls_file)

    all_project_data = []
    updated_urls = []

    for url, processed in urls:
        if processed:
            updated_urls.append((url, processed))
            continue

        # Check if data already exists in S3
        if check_if_data_exists(url):
            print(f"Data already exists for URL: {url}")
            updated_urls.append((url, True))
            continue

        # Scrape Kickstarter data
        print(f"Scraping data for URL: {url}")
        try:
            project_data = scrape_kickstarter(url)
        except Exception as e:
            print(f"Failed to scrape URL {url}: {e}")
            updated_urls.append((url, False))
            continue

        if not project_data:
            print(f"No data found for URL: {url}")
            updated_urls.append((url, False))
            continue
        
        all_project_data.append(project_data)
        updated_urls.append((url, True))

        # Save the scraped data to a file
        file_name = f"scraped_data_{url.replace('https://', '').replace('/', '_')}.json"
        with open(file_name, 'w') as f:
            json.dump([project_data], f)
        
        # Upload the scraped data to S3
        upload_file_to_s3(file_name, BUCKET_NAME)
    
    if not all_project_data:
        print("No new data found for any URLs.")
        return

    # Save the raw data to S3
    raw_data_file_name = "raw_data.json"
    with open(raw_data_file_name, 'w') as f:
        json.dump(all_project_data, f)
    upload_file_to_s3(raw_data_file_name, BUCKET_NAME)
    print("Raw data uploaded to S3.")

    # Preprocess data
    raw_data_df = pd.DataFrame(all_project_data)
    processed_data_df = preprocess_data(raw_data_df)
    processed_file_name = "processed_data.csv"
    processed_data_df.to_csv(processed_file_name, index=False)
    upload_file_to_s3(processed_file_name, BUCKET_NAME)
    print("Processed data uploaded to S3.")

    save_urls(urls_file, updated_urls)
    print("URLs file updated.")

    # Skip the training and prediction steps for now
    print("Data preprocessed and saved to the database.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pipeline.py <urls_file>")
        sys.exit(1)

    urls_file = sys.argv[1]
    main(urls_file)
