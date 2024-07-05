# Campaign Predictor

This project involves scraping data from Kickstarter campaigns, preprocessing the data, and uploading it to AWS S3. The process is managed through a pipeline that runs inside a Docker container.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.8+
- Docker
- Docker Compose
- AWS CLI configured with appropriate credentials

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/campaignPredictor.git
cd campaignPredictor
```
### 2. Setup Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r api/requirements.txt
```
### 3. AWS S3 Configuration
Ensure your AWS CLI is configured with the appropriate credentials and permissions to access the S3 bucket bucket-for-crowd-ai.

## Scraping Data Locally
1. Prepare URLs File
Create a file named data/urls.txt and list the Kickstarter campaign URLs you want to scrape, each on a new line.

2. Run the Scraper
```sh
python data/scraping/kickstarter_scraper.py data/urls.txt
```
This command will scrape the Kickstarter campaign data and save the results in the data/scraped_data directory.

## Running the Pipeline in Docker
1. Build Docker Image
```sh
docker-compose build
```
2. Run Docker Compose
```sh 
docker-compose up
```
This will start the Docker container, execute the pipeline script, process the scraped data, and upload the results to S3.

## Project Workflow

### Scrape Kickstarter Data Locally:

The scraper reads URLs from data/urls.txt.
Scrapes the campaign data using Selenium.
Saves the scraped data as JSON files in the data/scraped_data directory.

### Run Pipeline:

Docker container is built and run.
The pipeline script processes files in the data/scraped_data directory.
Checks if data already exists in S3 to prevent duplicates.
Uploads new data to S3.
Preprocesses the data and uploads the processed data to S3.

## Scripts
data/scraping/kickstarter_scraper.py
This script scrapes Kickstarter campaign data using Selenium and saves the results in the data/scraped_data directory.

scripts/pipeline.py
This script processes the locally scraped data, checks for duplicates in S3, uploads new data to S3, and preprocesses the data.

data/s3_utils.py
Contains utility functions for uploading and downloading files from S3.

data/preprocessing/preprocessing.py
Contains functions to preprocess the raw campaign data.

## Additional Notes
Ensure the data/scraped_data directory exists before running the pipeline.
The docker-compose.yml and Dockerfile are configured to set up the environment and execute the pipeline inside the Docker container.