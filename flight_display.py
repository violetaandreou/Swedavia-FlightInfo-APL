from datetime import datetime
from zoneinfo import ZoneInfo


def swedish_time(utc_value):
    if not utc_value:
        return "N/A"

    try:
        utc_dt = datetime.fromisoformat(
            utc_value.replace("Z", "+00:00")
        )
        local_dt = utc_dt.astimezone(
            ZoneInfo("Europe/Stockholm")
        )
        return local_dt.strftime("%Y-%m-%d %H:%M %Z")
    except (ValueError, TypeError):
        return "N/A"


def display_flight(flight):
    airline = flight.get("airlineOperator") or {}
    location = flight.get("locationAndStatus") or {}
    times = flight.get("arrivalTime") or flight.get("departureTime") or {}

    print("-" * 45)
    print("Flight:", flight.get("flightId", "N/A"))
    print("Airline:", airline.get("name", "N/A"))
    identifiers = flight.get("flightLegIdentifier") or {}
    departure_code = identifiers.get("departureAirportIata", "N/A")
    print("From:", flight.get("departureAirportEnglish") or departure_code)
    identifiers = flight.get("flightLegIdentifier") or {}
    arrival_code = identifiers.get("arrivalAirportIata", "N/A")
    print("To:", flight.get("arrivalAirportEnglish") or arrival_code)
    print("Status:", location.get("flightLegStatusEnglish", "N/A"))
    print("Terminal:", location.get("terminal", "N/A"))
    print("Gate:", location.get("gate", "N/A"))
    print("Scheduled Swedish time:", swedish_time(times.get("scheduledUtc")))
    print("-" * 45)
