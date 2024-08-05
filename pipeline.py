import subprocess

def run_script(script_path, *args):
    try:
        subprocess.run(['python3', script_path, *args], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_path}: {e}")

def log_message(message):
    try:
        subprocess.run(['node', 'dist/logging/logger.js', message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error logging message: {e}")

def update_urls_status(file_path, status_field, status_value):
    urls = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 3:
                if status_field == 'scraped':
                    urls.append((parts[0], status_value, parts[2]))
                elif status_field == 'uploaded':
                    urls.append((parts[0], parts[1], status_value))
            else:
                urls.append((parts[0], False, False))
    with open(file_path, 'w') as f:
        for url, scraped, uploaded in urls:
            f.write(f"{url} {scraped} {uploaded}\n")

if __name__ == "__main__":
    urls_file = 'urls.txt'
    
    log_message("Pipeline started")

    print("Running Kickstarter scraper...")
    run_script('./scripts/scraping/kickstarter_scraper.py', urls_file)
    update_urls_status(urls_file, 'scraped', True)

    print("Running Indiegogo scraper...")
    run_script('./scripts/scraping/indiegogo_scraper.py', urls_file)
    update_urls_status(urls_file, 'scraped', True)

    print("Combining data...")
    subprocess.run(['npm', 'run', 'start'], cwd='./scripts/preprocessing')

    print("Uploading data to AutoTrain...")
    subprocess.run(['npm', 'run', 'start'], cwd='./scripts/autotrain')
    update_urls_status(urls_file, 'uploaded', True)

    log_message("Pipeline completed successfully")
    print("Pipeline completed successfully.")