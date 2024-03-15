import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import urllib3
from time import sleep, strftime  # Import time library for sleep function

# Function to scrape data from a given page URL
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    records = []
    for listing in soup.find_all(class_="search-listing"):
        business_name = listing.find(class_="search-business-name").text.strip()
        address = listing.find(class_="search-busines-address").text.strip()
        phone_element = listing.find("a", class_="btn btn-yp-default mr-2 yp-click")
        phone = phone_element.get("href") if phone_element else None
        records.append((business_name, address, phone))

    return records


# URLs of pages to scrape
base_url = "https://www.yellow-pages.ph/search/grade-school-and-high-school/metro-manila/page-"
parts = base_url.split("/search")
parts = parts[1]
parts = parts.replace("/", "-")
parts = parts

# Starting and ending page (modify as needed)
start_page = 6 # start of the page
end_page = 20  # end of the page
# Example: scrape pages 2 to 5

# Scrape with interval
page_numbers = range(start_page, end_page + 1)  # Use range for inclusive end
records = []
for page_number in page_numbers:
    page_url = f"{base_url}{page_number}"
    page_records = scrape_page(page_url)
    records.extend(page_records)

    # Get current time with formatting
    current_time = strftime("%Y-%m-%d %H:%M:%S")  # Example format: 2024-03-15 15:23:12

    # Introduce 2-minute sleep between scraping pages
    print(f"Finished scraping page {page_number} at {current_time} at Sleeping for every 5 minutes...")
    sleep(300)  # Sleep for 300 seconds (5 minutes)

# Create DataFrame
df = pd.DataFrame(records, columns=["Business Name", "Address", "Phone"])

# Specify the folder path
folder_path = "scrape-folder"

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Save the DataFrame to CSV with the specified filename within the folder
df.to_csv(os.path.join(folder_path, f"{parts}{start_page}-{end_page}scape.csv"), index=False, mode='w')

print(f"CSV {parts}{start_page}-{end_page}scape.csv File has been created!")
