import requests
import json
import os

def fetch_and_save(url, output_file):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved data to {output_file}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

def main():
    prematch_url = "https://match-storage-partners.top-parser.com/lp-feed?lang=en&service=PREMATCH&sportId=25&startCoefficient=1.01&endDate=1746028418"
    fetch_and_save(prematch_url, "docs/prematch.json")

if __name__ == "__main__":
    main()
