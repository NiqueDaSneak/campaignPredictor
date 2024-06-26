import sys
import os
import pandas as pd

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from urllib.parse import urlparse
from data.scraping.kickstarter_scraper import scrape_kickstarter
from data.database import insert_raw_data, SessionLocal, engine
from data.preprocessing.preprocessing import preprocess_data
from models.training.train_model import train_model, save_model, load_model
from predict.predict import make_predictions

def read_urls(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    urls = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
    return urls

def mark_url_processed(file_path, url):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() == url:
                file.write(f'# {line.strip()} (processed)\n')
            else:
                file.write(line)

def clean_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

def main(urls_file):
    urls = read_urls(urls_file)

    session = SessionLocal()

    for url in urls:
        cleaned_url = clean_url(url)
        
        # Step 1: Scrape Kickstarter data
        print(f"Scraping Kickstarter data for URL: {cleaned_url}")
        project_data = scrape_kickstarter(cleaned_url)
        print("Data scraped:", project_data)

        # Step 2: Insert scraped data into the database
        print("Inserting data into the database...")
        try:
            if not insert_raw_data(session, project_data):
                print(f"Data for URL {cleaned_url} already exists in the database.")
                mark_url_processed(urls_file, url)
                continue
            mark_url_processed(urls_file, url)
        except Exception as e:
            print(f"Error inserting data for URL {cleaned_url}: {e}")

    session.close()

    # Step 3: Preprocess the data
    print("Preprocessing data...")
    session = SessionLocal()
    raw_data_df = pd.read_sql("SELECT * FROM raw_campaign_data", con=engine)
    processed_data_df = preprocess_data(raw_data_df)
    processed_data_df.to_sql("processed_campaign_data", con=engine, if_exists="replace", index=False)
    print("Data preprocessed and saved to the database.")
    session.close()

    # Prepare features (X) and target (y) for training
    X = processed_data_df.drop(columns=["pledged_amount", "url"])  # Exclude 'url' from features
    y = processed_data_df["pledged_amount"]

    # Step 4: Train the model
    print("Training model...")
    model = train_model(X, y)
    model_path = "models/training/model.joblib"
    save_model(model, model_path)
    print(f"Model trained and saved to {model_path}")

    # Step 5: Make predictions
    print("Making predictions...")
    model = load_model(model_path)
    predictions = make_predictions(model, X)
    print("Predictions:", predictions)

    # Optionally save predictions
    predictions_df = pd.DataFrame(predictions, columns=["Prediction"])
    predictions_df.to_csv("predictions.csv", index=False)
    print("Predictions saved to predictions.csv")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pipeline.py <URLs_File_Path>")
        sys.exit(1)

    urls_file = sys.argv[1]
    main(urls_file)
