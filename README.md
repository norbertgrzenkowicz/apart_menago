# apart_menago - Booking.com Scraper for Apartments Analysis

![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue)
![License](https://img.shields.io/badge/license-MIT-green)

apart_menago is a web scraping tool that gathers information about available apartments from Booking.com in the charming coastal towns of Władysławowo, Jastrzębia Góra, and Rozewie. This tool uses Beautiful Soup to scrape data, manipulates data with pandas, stores the data in PostgreSQL, and generates a customized newsletter email based on the specified client preferences.
## Features

- Scrape apartment data from Booking.com in Władysławowo, Jastrzębia Góra, and Rozewie using Beautiful Soup.
- View scrapped data on https:/localhost:5000.
- Store gathered data in a PostgreSQL database for easy retrieval and management.
- Generate newsletter emails with custom data output and analysis tailored to client specifications.

## Getting Started

These instructions will help you set up the project and start scraping apartment data.

### Prerequisites

- Python 3.12
- pip package manager
- PostgreSQL database
- SMTP server for sending emails

### Installation

1. Get a docker and docker compose on your machine.
2. Clone Repo.
3. Do a:
   ```bash
   docker compose build
   ```
   Then:
   ```bash
   docker compose up
   ```
   Open up a https://localhost:5000 and admire the results.

### Tests

   If u install locally with a venv:
   ```bash
   python3 -m venv venv && source venv/bin/activate
   ```
   U can run tests like this:
   ```bash
   python -m pytest -s src/interface.py
   ```
### Running
   With local set up u can run:
   ```bash
   python -m src.interface --help
   ```
   To see what possible args you can use.
   If u run:
   ```bash
   python -m src.interface
   ```
   You'll get default values for scrapping data configuration.
   Potentially it can look like this:
   ```bash
   python -m src.interface --city Wladyslawowo --start_date=2024-08-01 --end_date=2024-08-05 --people=4 --rooms=1 --timeofstay=4
   ```
   Make sure to have correct (not in the past) data in Y-M-D format.


5. Check your email for the generated newsletter.
   I think it's good idea to send this data directly on email in csv/xml/xslx form so thats a TODO. Possibility to send emails are in code already.
## Disclaimer

This project is for educational and informational purposes only. The developer is not responsible for the usage of the scraped data, database management, email distribution, or any legal implications that may arise from their use.

---

Experience the power of apart_menago - from scraping to database management to customized newsletters! If you encounter any issues or have suggestions for improvement, please feel free to open an issue or contribute to the repository.
