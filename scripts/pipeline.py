import os
import pandas as pd
import json

from data.s3_utils import upload_file_to_s3, download_file_from_s3
from data.preprocessing.preprocessing import preprocess_data
from data.scraping.kickstarter_scraper import scrape_kickstarter
from data.scraping.indiegogo_scraper import scrape_indiegogo

BUCKET_NAME = "bucket-for-crowd-ai"

def check_if_data_exists(url):
    file_name = f"scraped_data_{url.replace('https://', '').replace('/', '_')}.json"
    print(f"Checking if data exists in S3 for {file_name}")
    try:
        download_file_from_s3(BUCKET_NAME, file_name)
        print(f"Data exists in S3 for {file_name}")
        return True
    except Exception as e:
        print(f"No data in S3 for {file_name}: {e}")
        return False

def scrape_url(url):
    if "kickstarter.com" in url:
        return scrape_kickstarter(url)
    elif "indiegogo.com" in url:
        return scrape_indiegogo(url)
    else:
        print(f"Unknown URL format: {url}")
        return None

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

def main():
    data_dir = "data/scraped_data"
    urls_file = "data/urls.txt"
    all_project_data = []
    files_to_delete = []

    if not os.path.exists(data_dir):
        print(f"No directory found at {data_dir}")
        return

    urls = load_urls(urls_file)
    updated_urls = []

    for url, processed in urls:
        if processed:
            updated_urls.append((url, processed))
            continue

        print(f"Scraping data for URL: {url}")
        project_data = scrape_url(url)
        
        if project_data:
            # Save to JSON file
            file_name = f"scraped_data_{url.replace('https://', '').replace('/', '_')}.json"
            with open(os.path.join(data_dir, file_name), 'w') as f:
                json.dump(project_data, f)
            
            # Check if data already exists in S3
            if check_if_data_exists(project_data['url']):
                print(f"Data already exists for URL: {project_data['url']}")
                continue

            all_project_data.append(project_data)
            files_to_delete.append(os.path.join(data_dir, file_name))
            print(f"Added data for URL: {project_data['url']}")
            updated_urls.append((url, True))
        else:
            updated_urls.append((url, False))

    save_urls(urls_file, updated_urls)

    if not all_project_data:
        print("No new data found for any URLs.")
        return

    print(f"Uploading {len(all_project_data)} projects to S3")

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

    # Delete local files after uploading
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    print("Data preprocessed and saved to the database.")

if __name__ == "__main__":
    print("Pipeline script is starting...")
    main()
