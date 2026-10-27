import os
import time
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.swedavia.se/flightinfo/v2"


def automatic_demo():
    print("\n=== SWEDAVIA AUTOMATIC DEMO ===")

    api_key = os.getenv("SWEDAVIA_API_KEY")

    if not api_key:
        print("ERROR: API key is missing.")
        return

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Accept": "application/json"
    }

    date = datetime.now().strftime("%Y-%m-%d")
    short_date = datetime.now().strftime("%y%m%d")

    tests = [
        (
            "Arrivals - Stockholm Arlanda",
            f"{BASE_URL}/ARN/arrivals/{date}",
            None
        ),
        (
            "Departures - Stockholm Arlanda",
            f"{BASE_URL}/ARN/departures/{date}",
            None
        ),
        (
            "OData Query - Stockholm Arlanda",
            f"{BASE_URL}/query",
            {
                "filter": (
                    f"airport eq 'ARN' and "
                    f"scheduled eq '{short_date}' and "
                    "flightType eq 'A'"
                ),
                "count": 5
            }
        )
    ]

    passed = 0

    for name, url, params in tests:
        print(f"\nTesting: {name}")

        try:
            start = time.perf_counter()
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=20
            )
            elapsed = time.perf_counter() - start

            response.raise_for_status()
            data = response.json()
            flights = data.get("flights", [])

            print("HTTP Status:", response.status_code)
            print("Flights returned:", len(flights))
            print(f"Response time: {elapsed:.2f} seconds")
            print("Result: PASS")
            passed += 1

        except (requests.RequestException, ValueError) as error:
            print("Result: FAIL")
            print("Error:", type(error).__name__)

    print("\n=== DEMO SUMMARY ===")
    print(f"Tests passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("All API tests passed!")
    else:
        print("Some API tests failed.")


if __name__ == "__main__":
    automatic_demo()
