import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to do the scraping
def get_data_from_webpage(url):
    # Using headers to avoid blocking
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML)'
               }

    # Sending a HTTP request to the webpage
    response = requests.get(url)

    # Checking if the request succeeded
    if response.status_code != 200:
        print(f"Error accessing the page {url}. Status code: {response.status_code}")
        return []
    
    # Creating a BeautifulSoup object to analyze the page content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finding the table or part of the page that contains the data
    # This example assumes that the data are stored in a table <table> and that the columns are named "Name", "Latitude", "Longitude".
    # It may be necessary to adapt depending on the page structure
    data = []

    # Supposing that the table has lines <tr> with <td> for the columns
    for row in soup.find_all('tr'): # For each line of the table
        cols = row.find_all('td') # Finding the line cells
        if len(cols) > 0: # Making sure that there's data
            order = cols[0].get_text(strip=True)
            county_name = cols[1].get_text(strip=True)
            country = cols[2].get_text(strip=True)
            latitude = cols[3].get_text(strip=True)
            longitudee = cols[4].get_text(strip=True)
            #x = cols[5].get_text(strip=True)

            # Adding data into the list
            data.append([order, county_name, country, latitude, longitudee])

    return data

# Function to retreive the data from multiple pages and consolidate into a single DataFrame
def scrape_all_pages(start_page, end_page):
    all_data = []

    for page_num in range(start_page, end_page + 1):
        # Page URL for Scraping
        url = 'https://geokeo.com/database/county/ca/{page_nume}/'
        print(f"Retrieving data from page # {page_num} ...")

        # Retrieving data
        page_data = get_data_from_webpage(url)

        if page_data:
            all_data.extend(page_data)

        # Adds a break to avoid server overload
        time.sleep(1)
    
    return all_data

# Scraping pages 1 through 22
start_page = 1
end_page = 22
all_data = scrape_all_pages(start_page, end_page)

# Converting data into a Pandas DataFrame
df = pd.DataFrame(all_data, columns=["Order", "County_Name", "Country", "Latitude", "Longitude"])

# Extracting data
print(df)

# Importing to CSV
# df.to_csv('Canadian_County_Data.csv', index=False)