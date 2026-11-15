# Web Automation

Part 3 builds a small web data collector. It retrieves posts from the
JSONPlaceholder public test API and writes selected fields to a CSV report.

## Setup

From this directory, create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependency:

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

The report is created at `output/posts_report.csv`. The script uses a request
timeout, checks HTTP errors, validates the response shape, and exits with an
error message if the request or report generation fails.

JSONPlaceholder is a test service, so this project does not require credentials
or modify persistent data.
