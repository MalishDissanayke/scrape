import requests
import json

def fetch_data():
    url = "https://example.com/api/v1/sportsdata"  # Replace with actual API endpoint or URL
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def filter_data(data):
    prematch_data = [item for item in data if item['status'] == 'prematch']
    live_data = [item for item in data if item['status'] == 'live']
    return prematch_data, live_data

def save_data():
    data = fetch_data()
    
    if data:
        prematch_data, live_data = filter_data(data)

        # Save the filtered data to files
        with open('docs/prematch.json', 'w') as f:
            json.dump(prematch_data, f)

        with open('docs/live.json', 'w') as f:
            json.dump(live_data, f)

        print("Data saved successfully.")
    else:
        print("No data to save.")

if __name__ == "__main__":
    save_data()
