import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to do the scraping
def get_data_from_webpage(url):
    # Sending a HTTP request to the webpage
    response = requests.get(url)

    # Checking if the request succeeded
    if response.status_code != 200:
        print(f"Error accessing the page: {response.status_code}")
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

# Page URL for Scraping
url = 'https://geokeo.com/database/county/ca/1/'

# Retrieving data
data = get_data_from_webpage(url)

# Converting data into a Pandas DataFrame
df = pd.DataFrame(data, columns=["Order", "County_Name", "Country", "Latitude", "Longitude"])

# Extracting data
print(df)

# Importing to CSV
# df.to_csv('Canadian_County_Data.csv', index=False)