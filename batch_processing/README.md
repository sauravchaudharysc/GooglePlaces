# Google Places Batch Processor

This script reads Google Place IDs from `place_ids.csv`, calls the Google Places API, and extracts the place name, short address, and one photo.

Before running, open `batch_place_processor.py` and replace `API_KEY = "YOUR_GOOGLE_API_KEY"` with your actual Google Places API key.

Install dependency using `pip install requests`.

Run the script using `python batch_place_processor.py`.

Successful results will be saved in `places_output.jsonl`, and failed Place IDs will be saved in `deadletter.txt`.