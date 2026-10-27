import json
import os
import requests
from collections import Counter
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.swedavia.se/flightinfo/v2"

def show_destinations():
    airport = input("Enter airport code (default ARN): ").strip().upper() or "ARN"
    date = input("Enter date (YYYY-MM-DD), or Enter for today: ").strip()

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    flight_type = input("Arrivals (A) or Departures (D): ").strip().upper()

    if flight_type not in ("A", "D"):
        print("Invalid choice.")
        return

    endpoint = "arrivals" if flight_type == "A" else "departures"
    city_field = "departureAirportEnglish" if flight_type == "A" else "arrivalAirportEnglish"

    try:
        response = requests.get(
            f"{BASE_URL}/{airport}/{endpoint}/{date}",
            headers={
                "Ocp-Apim-Subscription-Key": os.getenv("SWEDAVIA_API_KEY"),
                "Accept": "application/json"
            },
            timeout=20
        )
        response.raise_for_status()

        flights = response.json().get("flights", [])
        cities = Counter(
            flight.get(city_field)
            for flight in flights
            if flight.get(city_field)
            and flight.get(city_field).strip().lower() not in ("unknown", "n/a")
        )

        print(f"\nTotal flight records: {len(flights)}")
        print(f"Unique destinations/origins: {len(cities)}")
        with open("city_country.json", encoding="utf-8") as file:
            city_to_country = json.load(file)["city_to_country"]

        print("\nCity                  Country              Flights")
        print("-" * 55)

        for city, count in cities.most_common():
            country = city_to_country.get(city.lower(), "Unknown")
            print(f"{city:<25}{country:<28}{count}")

    except (requests.RequestException, ValueError) as error:
        print("Error:", type(error).__name__)


if __name__ == "__main__":
    show_destinations()
