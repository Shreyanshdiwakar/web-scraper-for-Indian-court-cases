# Indian Court Cases Web Scraper

## Overview
This Python script scrapes court case details from IndianKanoon.org, specifically focusing on murder cases from Gujarat in 2016. The script uses Selenium with undetected-chromedriver to navigate the website and BeautifulSoup for parsing HTML content.

## Features
- Automated web scraping of court case details
- Handles pagination automatically 
- Extracts case titles, links, and full content
- Saves data to CSV format
- Built-in delays and error handling
- Multiple content extraction methods for reliability

## Components

### Main Functions

1. `get_driver()`
   - Creates and configures Chrome WebDriver
   - Sets up browser options for automation
   - Returns configured driver instance

2. `get_case_details(driver, case_url)`
   - Navigates to individual case pages
   - Handles "View Complete document" links
   - Uses multiple methods to extract case content:
     - doc2 class content
     - highlighted text
     - document content blocks
   - Includes error handling and retry mechanisms

3. `scrape_page(driver, url)`
   - Scrapes all cases from a single page
   - Extracts case titles and links
   - Calls get_case_details for each case
   - Returns list of (title, link, content) tuples

4. `main()`
   - Controls the overall scraping process
   - Handles pagination
   - Saves results to cases.csv
   - Includes error handling and cleanup

## Output
The script generates a CSV file (cases.csv) with three columns:
- Case Title
- Case Link 
- Case Content

## Dependencies
- undetected_chromedriver
- beautifulsoup4
- time
- csv

## Usage
1. Install required dependencies:
```bash
pip install undetected-chromedriver beautifulsoup4
```

2. Run the script:
```bash
python main.py
```

## Error Handling
- Built-in delays to prevent rate limiting
- Multiple content extraction methods for reliability
- Exception handling for network issues
- Graceful termination and cleanup

## Notes
- The script includes appropriate delays to avoid overwhelming the server
- Chrome browser is required for the script to work
- Internet connection is required throughout the scraping process
- The script may take significant time depending on the number of cases

## Legal Notice
Ensure compliance with IndianKanoon.org's terms of service and robots.txt before using this scraper. Consider rate limiting and fair use policies.

## License
MIT License
