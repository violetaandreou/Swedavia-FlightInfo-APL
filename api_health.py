import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def check_api_health():
    print("\nChecking Swedavia API connection...")

    api_key = os.getenv("SWEDAVIA_API_KEY")

    if not api_key:
        print("ERROR: API key is missing.")
        return

    date = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.swedavia.se/flightinfo/v2/ARN/arrivals/{date}"

    try:
        start = time.perf_counter()

        response = requests.get(
            url,
            headers={
                "Ocp-Apim-Subscription-Key": api_key,
                "Accept": "application/json"
            },
            timeout=20
        )

        elapsed = time.perf_counter() - start

        print("HTTP Status:", response.status_code)
        print(f"Response time: {elapsed:.2f} seconds")

        if response.status_code == 200:
            print("API Health: HEALTHY")
            print("Connection successful!")
        else:
            print("API Health: FAILED")

    except requests.RequestException as error:
        print("API Health: FAILED")
        print("Error:", type(error).__name__)


if __name__ == "__main__":
    check_api_health()
