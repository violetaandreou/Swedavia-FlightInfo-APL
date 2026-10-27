import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from flight_display import display_flight

load_dotenv()

BASE_URL = "https://api.swedavia.se/flightinfo/v2"


def query_flights(airport="ARN", flight_type="A", date=None):
    if date is None:
        date = datetime.now().strftime("%y%m%d")

    filter_text = (
        f"airport eq '{airport}' and "
        f"scheduled eq '{date}' and "
        f"flightType eq '{flight_type}'"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": os.getenv("SWEDAVIA_API_KEY"),
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            f"{BASE_URL}/query",
            headers=headers,
            params={"filter": filter_text, "count": 5},
            timeout=20
        )
        response.raise_for_status()

        data = response.json()
        flights = data.get("flights", [])

        print(f"\nOData Query successful!")
        print(f"Flights returned: {len(flights)}")

        for item in flights:
            flight = item.get("arrival") or item.get("departure") or item
            display_flight(flight)

        if data.get("continuationToken"):
            print("More flights are available through pagination.")

    except (requests.RequestException, ValueError) as error:
        print("OData error:", type(error).__name__)


if __name__ == "__main__":
    query_flights()
