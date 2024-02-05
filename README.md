# apart_menago - Booking.com Scraper for Apartments Analysis

![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue)
![License](https://img.shields.io/badge/license-MIT-green)

apart_menago is a web scraping tool that gathers information about available apartments from Booking.com in the charming coastal towns of Władysławowo, Jastrzębia Góra, and Rozewie. This tool uses Beautiful Soup to scrape data, manipulates data with pandas, stores the data in PostgreSQL, and generates a customized newsletter email based on the specified client preferences.

## Features

- Scrape apartment data from Booking.com in Władysławowo, Jastrzębia Góra, and Rozewie using Beautiful Soup.
- Manipulate and analyze scraped data using pandas.
- Store gathered data in a PostgreSQL database for easy retrieval and management.
- Generate newsletter emails with custom data output and analysis tailored to client specifications.
- Easy-to-use configuration for specifying scraping criteria, database connection, and email preferences.

## Getting Started

These instructions will help you set up the project and start scraping apartment data.

### Prerequisites

- Python 3.8 or 3.9
- pip package manager
- PostgreSQL database
- SMTP server for sending emails

### Installation

1. Clone the repository.

2. Navigate to the project directory:

   ```bash
   cd apart_menago
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

   For now the best and only way to use script is to run a tests. Command below will do the work to run a scrapper through interface.py script.

   ```bash
   python -m pytest -s interface.py
   ```

   The scraper will start collecting apartment data based on your preferences, store it in the PostgreSQL database, and generate a newsletter email with customized data analysis (NOT IMPLEMENTED).

### Web menago Usage

   ```bash
   sudo /etc/init.d/postgresql restart
   cd apart_menago_web
   python manage.py runserver
   ```

5. Check your email for the generated newsletter.

## Configuration

- `config.py`: Edit scraping preferences, locations, check-in/out dates, and more.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational and informational purposes only. The developer is not responsible for the usage of the scraped data, database management, email distribution, or any legal implications that may arise from their use.

---

Experience the power of apart_menago - from scraping to database management to customized newsletters! If you encounter any issues or have suggestions for improvement, please feel free to open an issue or contribute to the repository.
