import csv
import json
import time
import requests
from typing import Dict, Any, List, Optional


API_KEY = "<API_KEY>"

INPUT_CSV_FILE = "place_ids.csv"
OUTPUT_JSONL_FILE = "places_output.jsonl"
DEADLETTER_FILE = "deadletter.txt"

BATCH_SIZE = 100
REQUEST_DELAY_SECONDS = 0.1
MAX_RETRIES = 3


def read_place_ids_from_csv(file_path: str) -> List[str]:
    """
    Reads place_id values from CSV file.
    Expected column name: place_id
    """

    place_ids = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            place_id = row.get("place_id")

            if place_id:
                place_ids.append(place_id.strip())

    return place_ids


def create_batches(items: List[str], batch_size: int):
    """
    Splits list into batches.
    """

    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def fetch_place_details(place_id: str) -> Dict[str, Any]:
    """
    Calls Google Places API for a single place_id.
    Fetches only required fields:
    - displayName
    - shortFormattedAddress
    - photos
    """

    url = f"https://places.googleapis.com/v1/places/{place_id}"

    headers = {
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "displayName,shortFormattedAddress,photos"
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    return response.json()


def fetch_with_retry(place_id: str) -> Optional[Dict[str, Any]]:
    """
    Retries Google API call if it fails.
    Returns API response if successful.
    Returns None if all retries fail.
    """

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fetch_place_details(place_id)

        except requests.exceptions.RequestException as e:
            print(
                f"Attempt {attempt}/{MAX_RETRIES} failed for place_id={place_id}. "
                f"Error: {str(e)}"
            )

            if attempt < MAX_RETRIES:
                sleep_time = attempt * 2
                time.sleep(sleep_time)

    return None


def extract_required_fields(place_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts only the fields needed for SQL DB storage.
    """

    photos = data.get("photos", [])
    photo_name = photos[0].get("name") if photos else None

    photo_url = None
    if photo_name:
        photo_url = (
            f"https://places.googleapis.com/v1/{photo_name}/media"
            f"?maxWidthPx=800&key={API_KEY}"
        )

    return {
        "place_id": place_id,
        "display_name": data.get("displayName", {}).get("text"),
        "short_formatted_address": data.get("shortFormattedAddress"),
        "place_photo_name": photo_name,
        "place_photo_url": photo_url
    }


def write_success_record(record: Dict[str, Any]) -> None:
    """
    Writes one successful record to JSONL output file.
    JSONL means one JSON object per line.
    This is suitable for large files and DB imports.
    """

    with open(OUTPUT_JSONL_FILE, mode="a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_deadletter(place_id: str, reason: str = "") -> None:
    """
    Stores failed place_id in deadletter.txt.
    """

    with open(DEADLETTER_FILE, mode="a", encoding="utf-8") as file:
        file.write(f"{place_id}")
        if reason:
            file.write(f" | {reason}")
        file.write("\n")


def process_batch(batch: List[str], batch_number: int, total_batches: int) -> None:
    """
    Processes one batch of place_ids.
    """

    print(f"\nProcessing batch {batch_number}/{total_batches}")
    print(f"Batch size: {len(batch)}")

    for index, place_id in enumerate(batch, start=1):
        print(f"Processing {index}/{len(batch)} in batch {batch_number}: {place_id}")

        api_response = fetch_with_retry(place_id)

        if api_response is None:
            write_deadletter(place_id, "API request failed after retries")
            continue

        try:
            formatted_record = extract_required_fields(place_id, api_response)

            if not formatted_record["display_name"]:
                write_deadletter(place_id, "Missing display_name")
                continue

            write_success_record(formatted_record)

        except Exception as e:
            write_deadletter(place_id, f"Parsing failed: {str(e)}")

        time.sleep(REQUEST_DELAY_SECONDS)


def main():
    print("Starting Google Places batch processing...")

    place_ids = read_place_ids_from_csv(INPUT_CSV_FILE)

    if not place_ids:
        print("No place_ids found in CSV.")
        return

    total_records = len(place_ids)
    total_batches = (total_records + BATCH_SIZE - 1) // BATCH_SIZE

    print(f"Total place_ids found: {total_records}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Total batches: {total_batches}")

    for batch_number, batch in enumerate(create_batches(place_ids, BATCH_SIZE), start=1):
        process_batch(batch, batch_number, total_batches)

    print("\nProcessing completed.")
    print(f"Successful records saved in: {OUTPUT_JSONL_FILE}")
    print(f"Failed place_ids saved in: {DEADLETTER_FILE}")


if __name__ == "__main__":
    main()