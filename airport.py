from date_validation import validate_date
from flight_display import display_flight
from odata_query import query_flights
from api_health import check_api_health
from automatic_demo import automatic_demo
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWEDAVIA_API_KEY")
BASE_URL = "https://api.swedavia.se/flightinfo/v2"

AIRPORTS = {
    "ARN": "Stockholm Arlanda",
    "GOT": "Göteborg Landvetter",
    "BMA": "Stockholm Bromma",
    "MMX": "Malmö",
    "LLA": "Luleå",
    "UME": "Umeå",
    "OSD": "Östersund",
    "VBY": "Visby",
    "RNB": "Ronneby",
    "KRN": "Kiruna"
}

def get_flights(flight_type):
    print("\nAvailable airports:")
    for code, name in AIRPORTS.items():
        print(f"{code} - {name}")

    airport = input("\nEnter airport code: ").strip().upper()

    if airport not in AIRPORTS:
        print("Invalid airport code.")
        return

    date = input("Enter date (YYYY-MM-DD), or press Enter for today: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    if not validate_date(date):
        print("Invalid date. Please use YYYY-MM-DD.")
        return

    url = f"{BASE_URL}/{airport}/{flight_type}/{date}"

    try:
        response = requests.get(
            url,
            headers={
                "Ocp-Apim-Subscription-Key": API_KEY,
                "Accept": "application/json"
            },
            timeout=20
        )
        response.raise_for_status()
        flights = response.json().get("flights", [])

        print(f"\nFound {len(flights)} flights.")
        page_size = 50

        for start in range(0, len(flights), page_size):
            page = flights[start:start + page_size]

            for flight in page:
                display_flight(flight)

            shown = min(start + page_size, len(flights))
            remaining = len(flights) - shown

            print(f"\nShowing {shown}/{len(flights)} flights ({remaining} remaining)")

            if remaining == 0:
                break

            choice = input(
                "[Enter] Next page | [a] Show all | [q] Back to menu: "
            ).strip().lower()

            if choice == "q":
                break
            elif choice == "a":
                for flight in flights[shown:]:
                    display_flight(flight)
                break

    except requests.RequestException as error:
        print("API error:", type(error).__name__)



def search_flight():
    print("\nSearch for a flight")
    flight_number = input("Enter flight number: ").strip().upper()

    if not flight_number:
        print("Please enter a flight number.")
        return

    print("\nAvailable airports:")
    for code, name in AIRPORTS.items():
        print(f"{code} - {name}")

    airport = input("\nEnter airport code: ").strip().upper()

    if airport not in AIRPORTS:
        print("Invalid airport code.")
        return

    date = input("Enter date (YYYY-MM-DD), or press Enter for today: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    if not validate_date(date):
        print("Invalid date. Please use YYYY-MM-DD.")
        return

    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Accept": "application/json"
    }

    found = []

    for flight_type in ("arrivals", "departures"):
        url = f"{BASE_URL}/{airport}/{flight_type}/{date}"

        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()

            flights = response.json().get("flights", [])

            for flight in flights:
                if str(flight.get("flightId", "")).upper() == flight_number:
                    found.append(flight)

        except (requests.RequestException, ValueError) as error:
            print(f"Could not check {flight_type}: {type(error).__name__}")
            return

    if found:
        print(f"\nFound {len(found)} matching flights.")
        for flight in found:
            display_flight(flight)
    else:
        print("No matching flight found.")

def main():
    while True:
        print("\nSwedavia FlightInfo")
        print("1. Arrivals")
        print("2. Departures")
        print("3. Search Flight")
        print("4. OData Query")
        print("5. API Health Check")
        print("6. Automatic Demo")
        print("q. Exit")

        choice = input("\nChoose an option: ").strip().lower()

        if choice == "1":
            get_flights("arrivals")
        elif choice == "2":
            get_flights("departures")
        elif choice == "3":
            search_flight()
        elif choice == "4":
            print("\nOData Flight Search")

            airport = input("Airport code (default ARN): ").strip().upper() or "ARN"

            if airport not in AIRPORTS:
                print("Invalid airport code.")
                continue

            flight_type = input(
                "Arrivals (A) or Departures (D), default A: "
            ).strip().upper() or "A"

            if flight_type not in ("A", "D"):
                print("Invalid flight type.")
                continue

            date = input(
                "Date (YYMMDD), or Enter for today: "
            ).strip()

            if date:
                try:
                    datetime.strptime(date, "%y%m%d")
                except ValueError:
                    print("Invalid date. Please use YYMMDD.")
                    continue

            query_flights(airport, flight_type, date or None)
        elif choice == "5":
            check_api_health()
        elif choice == "6":
            automatic_demo()
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
