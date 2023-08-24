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

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/apart_menago.git
   ```

2. Navigate to the project directory:

   ```bash
   cd apart_menago
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Configure your scraping preferences in the `config.yaml` file. You can specify search parameters, filters, and output options.

2. Set up your PostgreSQL database by editing the `database.yaml` file with your database connection details.

3. Configure email settings in the `email.yaml` file, including SMTP server details and email recipients.

4. Run the scraper:

   ```bash
   python scrape.py
   ```

   The scraper will start collecting apartment data based on your preferences, store it in the PostgreSQL database, and generate a newsletter email with customized data analysis.

5. Check your email for the generated newsletter.

## Configuration

- `config.yaml`: Edit scraping preferences, locations, check-in/out dates, and more.
- `database.yaml`: Configure PostgreSQL database connection details.
- `email.yaml`: Set up email preferences, including SMTP server information and recipients.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational and informational purposes only. The developer is not responsible for the usage of the scraped data, database management, email distribution, or any legal implications that may arise from their use.

---

Experience the power of apart_menago - from scraping to database management to customized newsletters! If you encounter any issues or have suggestions for improvement, please feel free to open an issue or contribute to the repository.
