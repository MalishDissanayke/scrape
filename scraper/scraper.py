import requests
from bs4 import BeautifulSoup
import json

def fetch_data():
    url = "https://1wywg.com/v3/3991/landing-betting-india?p=zgpn&sub1=14t2n34f8hpef"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Data fetched successfully.")
        return response.text
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    prematch_data = []
    live_data = []

    # Update the parsing based on the actual HTML structure
    betting_cards = soup.find_all('div', class_='betting-card')  # Change 'betting-card' to the correct class name
    
    for card in betting_cards:
        match_name = card.find('span', class_='match-name').text if card.find('span', class_='match-name') else 'N/A'
        odds = card.find('span', class_='odds').text if card.find('span', class_='odds') else 'N/A'
        match_time = card.find('span', class_='match-time').text if card.find('span', class_='match-time') else 'N/A'

        match_data = {
            'match_name': match_name,
            'odds': odds,
            'match_time': match_time,
        }
        
        if 'prematch' in match_time.lower():
            prematch_data.append(match_data)
        else:
            live_data.append(match_data)
    
    print(f"Prematch data: {len(prematch_data)} entries.")
    print(f"Live data: {len(live_data)} entries.")
    
    return prematch_data, live_data

def save_data(prematch_data, live_data):
    if prematch_data or live_data:
        with open('docs/prematch.json', 'w') as f:
            json.dump(prematch_data, f, indent=4)

        with open('docs/live.json', 'w') as f:
            json.dump(live_data, f, indent=4)
        
        print("Data saved successfully.")
    else:
        print("No new data to save.")

def main():
    html_content = fetch_data()
    if html_content:
        prematch_data, live_data = parse_data(html_content)
        save_data(prematch_data, live_data)

if __name__ == "__main__":
    main()
