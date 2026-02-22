import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_shipment_data(api_url):
    try:
        logger.info(f"Fetching shipment data from {api_url}")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info("Shipment data fetched successfully")
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching shipment data: {e}")
        return None

def fetch_weather_alerts(api_url):
    try:
        logger.info(f"Fetching weather alerts from {api_url}")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info("Weather alerts fetched successfully")
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching weather alerts: {e}")
        return None

def fetch_strike_news(api_url):
    try:
        logger.info(f"Fetching strike news from {api_url}")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info("Strike news fetched successfully")
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching strike news: {e}")
        return None

def main():
    # Example URLs (replace with actual)
    shipment_url = "https://api.example.com/shipments"
    weather_url = "https://api.weather.com/alerts"
    strike_url = "https://api.news.com/strikes"

    shipment_data = fetch_shipment_data(shipment_url)
    weather_data = fetch_weather_alerts(weather_url)
    strike_data = fetch_strike_news(strike_url)

    return {
        "shipments": shipment_data,
        "weather": weather_data,
        "strikes": strike_data
    }

if __name__ == "__main__":
    data = main()
    print(data)
