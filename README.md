# ListenBack Backend Setup Guide

## Prerequisites
- Python 3.12 or higher
- Google Cloud service account credentials

## Setup Steps

### 1. Create a Virtual Environment
```powershell
python -m venv .venv
```

### 2. Install Dependencies
Activate your virtual environment, then run:
```powershell
pip install -r requirements.txt
```

### 3. Configure Environment Variables
- Copy `.env.example` to `.env` and update the values as needed.
- Place the `.env` file in the project root folder.

### 4. Add Google Cloud Credentials
- Put your `service-account.json` file in the `credential/` folder.  
Note: You have to create your own `service-account.json` from google cloud console

## Running the Application
Run the backend server with:
```powershell
python src/app.py
```

The application will start on `localhost` at port `8000`.

http://localhost:8000  

## Folder Structure
- `src/` - Source code
- `credential/` - Google Cloud credentials
- `static/` - Static files
- `templates/` - HTML templates
- `docs/` - Documentation

## Additional Notes
- Ensure all required environment variables are set in `.env`.
- For API documentation, see files in the `docs/` folder.
