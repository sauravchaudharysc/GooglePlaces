# Google Places Web App

A responsive FastAPI web app that accepts a Google Place ID and returns:

- displayName.text
- shortFormattedAddress
- one place photo

## Local setup

1. Install Python 3.10+
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file:

```bash
GOOGLE_API_KEY=your_google_places_api_key_here
```

4. Run:

```bash
uvicorn main:app --reload
```

5. Open:

```text
http://127.0.0.1:8000
```

## Deploy on Render

1. Push this folder to GitHub.
2. Go to Render.
3. New + → Web Service.
4. Connect your GitHub repository.
5. Use these settings:

```text
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

6. Add environment variable:

```text
GOOGLE_API_KEY = your_google_places_api_key
```

7. Click Deploy.

## Important

Do not put your Google API key in frontend JavaScript. This project keeps the key in the backend.
