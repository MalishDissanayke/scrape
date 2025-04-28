import requests
from bs4 import BeautifulSoup
import json

def fetch_data():
    url = "https://1wywg.com/v3/3991/landing-betting-india?p=zgpn&sub1=14t2n34f8hpef"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    prematch_data = []
    live_data = []
    
    betting_cards = soup.find_all('div', class_='betting-card')
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
    
    return prematch_data, live_data

def save_data(prematch_data, live_data):
    with open('docs/prematch.json', 'w') as f:
        json.dump(prematch_data, f)

    with open('docs/live.json', 'w') as f:
        json.dump(live_data, f)

    print("Data saved successfully.")

def main():
    html = fetch_data()
    if html:
        prematch_data, live_data = parse_data(html)
        save_data(prematch_data, live_data)

if __name__ == "__main__":
    main()
