import requests
import json


API_KEY = "<API-Key>"  # Replace with your API key
PLACE_ID = "ChIJT5uBZwYeDTkRuJ11YPGVSYM"  # Replace with your place id


def fetch_place_details(place_id: str) -> dict:
    url = f"https://places.googleapis.com/v1/places/{place_id}"

    headers = {
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "displayName,shortFormattedAddress,photos"
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    return response.json()


def extract_required_fields(data: dict) -> dict:
    photos = data.get("photos", [])

    return {
        "displayName": data.get("displayName", {}).get("text"),
        "shortFormattedAddress": data.get("shortFormattedAddress"),
        "placePhoto": photos[0].get("name") if photos else None
    }


def main():
    try:
        api_response = fetch_place_details(PLACE_ID)

        final_data = extract_required_fields(api_response)

        print(json.dumps(final_data, indent=4, ensure_ascii=False))

        with open("place_output.json", "w", encoding="utf-8") as file:
            json.dump(final_data, file, indent=4, ensure_ascii=False)

        print("Saved to place_output.json")

    except requests.exceptions.RequestException as e:
        print("API request failed:", str(e))

    except Exception as e:
        print("Something went wrong:", str(e))


if __name__ == "__main__":
    main()