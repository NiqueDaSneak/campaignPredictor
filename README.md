<<<<<<< Updated upstream
=======

# Kickstarter Campaign Data Scraper

## Overview
This project scrapes Kickstarter campaign data, preprocesses it, and stores the results in an S3 bucket. The data is then used for analysis and model training.

## Setup Instructions

### Prerequisites
1. **Install Python 3.12+:** [Python Download](https://www.python.org/downloads/)
2. **Install Git:** [Git Download](https://git-scm.com/downloads)
3. **Install AWS CLI:** [AWS CLI Download](https://aws.amazon.com/cli/)

### Environment Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/campaignPredictor.git
   cd campaignPredictor
   ```

2. **Set up a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
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
   - List each Kickstarter campaign URL on a new line followed by a boolean indicating if it has been processed. Example:
     ```
     https://www.kickstarter.com/projects/example1 False
     https://www.kickstarter.com/projects/example2 False
     ```

2. **Run the pipeline:**
   ```sh
   python scripts/pipeline.py data/urls.txt
   ```

### Development Setup for VSCode
1. **Install VSCode:** [VSCode Download](https://code.visualstudio.com/)
2. **Open the project folder in VSCode:**
   ```sh
   code .
   ```

3. **Install Python extension for VSCode:**
   - Go to Extensions view by clicking the square icon in the sidebar or pressing `Ctrl+Shift+X`.
   - Search for "Python" and install the extension by Microsoft.

4. **Configure VSCode to use the virtual environment:**
   - Open the Command Palette by pressing `Ctrl+Shift+P`.
   - Type `Python: Select Interpreter` and select the virtual environment you created (it should be something like `venv/bin/python` or `venv\Scripts\python`).

### Contributing
1. **Fork the repository.**
2. **Create a new branch for your feature or bugfix.**
3. **Submit a pull request with a detailed description of changes.**

## Notes
- Ensure AWS credentials are configured correctly.
- The pipeline updates the `urls.txt` file with a processed flag to avoid reprocessing.

## `.gitignore`
Ensure the following is included in your `.gitignore` file to exclude unnecessary files from version control:
```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
.pytest_cache/
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# dotenv
.env
.env.*

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# AWS credentials
*.csv

# Visual Studio Code
.vscode/

# macOS
.DS_Store
```
>>>>>>> Stashed changes
