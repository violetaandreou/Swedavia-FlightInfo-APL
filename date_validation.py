from datetime import datetime


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    test_dates = [
        "2026-10-26",
        "2026-99-99",
        "hello",
        "2026-02-30"
    ]

    for date in test_dates:
        print(f"{date}: {validate_date(date)}")
