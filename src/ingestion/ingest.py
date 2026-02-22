import requests

def fetch_shipment_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_weather_alerts(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_strike_news(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None
