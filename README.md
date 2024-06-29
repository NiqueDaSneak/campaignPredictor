
# Kickstarter Campaign Data Scraper

## Overview
This project scrapes Kickstarter campaign data, preprocesses it, and stores the results in an S3 bucket. The data is then used for analysis and model training.

## Setup Instructions

### Environment Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/campaignPredictor.git
   cd campaignPredictor
   ```

2. **Set up a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure AWS CLI:**
   ```sh
   aws configure
   ```

### Running the Pipeline
1. **Prepare `urls.txt`:**
   - List each Kickstarter campaign URL on a new line. Example:
     ```
     https://www.kickstarter.com/projects/example1 True
     https://www.kickstarter.com/projects/example2 False
     ```

2. **Run the pipeline:**
   ```sh
   python scripts/pipeline.py data/urls.txt
   ```

### Contributing
1. **Fork the repository.**
2. **Create a new branch for your feature or bugfix.**
3. **Submit a pull request with a detailed description of changes.**

## Notes
- Ensure AWS credentials are configured correctly.
- The pipeline updates the `urls.txt` file with a processed flag to avoid reprocessing.
