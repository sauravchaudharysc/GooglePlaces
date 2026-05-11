import os
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI(title="Google Places Finder")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


def fetch_place_details(place_id: str) -> dict:
    if not GOOGLE_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_API_KEY is missing. Add it in .env locally or Environment Variables on Render."
        )

    url = f"https://places.googleapis.com/v1/places/{place_id}"

    headers = {
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "displayName,shortFormattedAddress,photos"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text
        raise HTTPException(status_code=response.status_code, detail=error_detail)
    except requests.exceptions.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Google API request failed: {str(exc)}")


def extract_required_fields(data: dict) -> dict:
    photos = data.get("photos", [])
    photo_name: Optional[str] = photos[0].get("name") if photos else None

    return {
        "displayName": data.get("displayName", {}).get("text"),
        "shortFormattedAddress": data.get("shortFormattedAddress"),
        "placePhotoName": photo_name,
        "placePhotoUrl": f"/api/photo?name={photo_name}" if photo_name else None
    }


@app.get("/api/place/{place_id}")
def get_place(place_id: str):
    api_response = fetch_place_details(place_id)
    return extract_required_fields(api_response)


@app.get("/api/photo")
def get_place_photo(name: str = Query(..., description="Google photo resource name")):
    """
    Proxies the Google photo through the backend so your API key is not exposed in frontend image URLs.
    """
    if not GOOGLE_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_API_KEY is missing."
        )

    media_url = f"https://places.googleapis.com/v1/{name}/media"

    params = {
        "maxWidthPx": 900,
        "key": GOOGLE_API_KEY
    }

    try:
        response = requests.get(media_url, params=params, timeout=25, stream=True)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "image/jpeg")

        return StreamingResponse(
            response.iter_content(chunk_size=8192),
            media_type=content_type
        )

    except requests.exceptions.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Photo request failed: {str(exc)}")
