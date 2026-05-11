# Google Places Web App

A modern FastAPI web application that accepts a Google Place ID and returns:

- `displayName.text`
- `shortFormattedAddress`
- One place photo

The application provides a clean UI and JSON-ready response format using the Google Places API.

## Live Demo

Try it here:

[Google Places Web App](https://googleplaces.onrender.com)


---

## Features

- FastAPI backend
- Responsive modern UI
- Google Places API integration
- Fetch place details using Place ID
- Display place photo dynamically
- JSON-ready structured response
- Copy JSON output button
- Clean and minimal frontend

---

## Tech Stack

- Python
- FastAPI
- HTML
- CSS
- JavaScript
- Google Places API

---

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Install Python 3.10+

Download Python from:

[Python Official Website](https://www.python.org/)

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
GOOGLE_API_KEY=your_google_places_api_key_here
```

Get your API key from:

[Google Cloud Console](https://console.cloud.google.com)

Enable:
- Places API (New)

---

## Run the Application

```bash
uvicorn main:app --reload
```

Open in browser:

```text
http://127.0.0.1:8000
```

---

## API Flow

1. User enters a Google Place ID
2. Backend calls Google Places API
3. Fetches:
   - Place name
   - Short address
   - Place photo
4. Returns structured response
5. Frontend renders UI dynamically
