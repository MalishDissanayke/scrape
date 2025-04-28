import requests
import json
import os

def fetch_and_save(url, filepath):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {filepath}")
    else:
        print(f"Failed to fetch {url}, status code {response.status_code}")

def main():
    prematch_url = "https://api.sportsapi365.com/api/v1/PreMatchEvents?lang=en&eventCount=20"
    live_url = "https://api.sportsapi365.com/api/v1/LiveEvents?lang=en&eventCount=20"

    fetch_and_save(prematch_url, "docs/prematch.json")
    fetch_and_save(live_url, "docs/live.json")

if __name__ == "__main__":
    main()
