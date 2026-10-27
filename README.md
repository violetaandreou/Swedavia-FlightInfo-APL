# Swedavia FlightInfo – APL Project 2026

## Introduction

This is my APL project, where I recreated a flight information application using Python and GenAI.

I watched a video showing the original application and used it as inspiration to build my own version.

The application uses the Swedavia FlightInfo API v2 to get flight information from Swedish airports.

## Tools and Technologies

- Python
- Visual Studio Code
- Swedavia FlightInfo API v2
- Requests
- Python-dotenv
- JSON
- Git and GitHub
- GenAI (ChatGPT)

## Features

The application includes:

1. Arrivals – Shows arriving flights.
2. Departures – Shows departing flights.
3. Search Flight – Searches for a specific flight number.
4. OData Query – Searches flights using filters.
5. API Health Check – Checks the API connection.
6. Automatic Demo – Tests three API requests automatically.

I also created destination statistics showing cities, countries and the number of flight records.

## My Improvements

I added several improvements:

- Displaying 50 flights at a time.
- Converting UTC time to Swedish time.
- Validating dates before making API requests.
- Showing flight details such as airline, airport, status and terminal.
- Displaying destination statistics by city and country.
- Handling missing information with fallback values.
- Keeping the API key in a private environment file.

## Installation

1. Install Python.
2. Download or clone this repository.
3. Create a virtual environment:

   python -m venv .venv

4. Activate the virtual environment.
5. Install the required packages:

   python -m pip install -r requirements.txt

6. Create a `.env` file and add:

   SWEDAVIA_API_KEY=your_api_key_here

7. Get an API key from the official Swedavia Developer Portal.

## Run the Application

Main application:

    python airport.py

Destination statistics:

    python destinationer.py

## Testing

Run the automated tests:

    python -m unittest discover -s tests -p "test_swedavia.py" -v

During development, all five automated tests passed.

The Automatic Demo also completed three API requests successfully.

## Problems and Solutions

During development, I experienced some problems:

- PowerShell blocked the virtual environment activation script.
- Python could not find the Swedish time zone because tzdata was missing.
- Some code changes did not match the original source correctly.
- A test file had an incorrect name, so Python could not discover the tests.

I solved these problems through troubleshooting and testing.

## GenAI

I used ChatGPT to help me recreate the application, generate Python code, troubleshoot errors and improve the functions.

I tested the results myself and made changes during development.

## Security

The API key is stored in a private `.env` file.

The `.gitignore` file prevents the API key and virtual environment from being uploaded to GitHub.

## Conclusion

This project helped me learn more about Python, APIs, JSON, testing and troubleshooting.

I also learned how to use GenAI during software development.
