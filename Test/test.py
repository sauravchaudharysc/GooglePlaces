
import requests
import json

API_KEY = "<API-Key>"
PLACE_ID = "ChIJT5uBZwYeDTkRuJ11YPGVSYM"

url = f"https://places.googleapis.com/v1/places/{PLACE_ID}"

headers = {
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "*"
}

response = requests.get(url, headers=headers)
data = response.json()

with open("sampleoutput.txt", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("Saved response to sampleoutput.txt")