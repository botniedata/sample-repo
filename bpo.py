from bs4 import BeautifulSoup
import pandas as pd

# Sample HTML content
with open("bpo.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize lists to store extracted data
names = []
addresses = []
nums = []
websites = []

# Find all <li> elements
list_items = soup.find_all('li', class_=lambda x: x and 'ln-' in x)

for item in list_items:
    # Extract name, address, and num using their class names
    name = item.find('h3', class_='name').text if item.find('h3', class_='name') else ''
    address = item.find('p', class_='address').text.strip().replace('\n', '').lower().title() if item.find('p', class_='address') else ''
    num = item.find('p', class_='num').text.strip() if item.find('p', class_='num') else ''
    website = item.find('a', class_='button').get('href') if item.find('a', class_='button') else ''
    
    # Append extracted data to respective lists
    names.append(name.replace('"', '').upper())
    addresses.append(address.replace('"', ''))  # Remove double quotes from the address
    nums.append(num)
    websites.append(website)

# Create DataFrame from extracted data
data = {'Name': names, 'Address': addresses, 'Number': nums, 'Website': websites}
df = pd.DataFrame(data)

# Replace NaN values with blank strings
df.fillna('', inplace=True)

# Export DataFrame to CSV file
df.to_csv(f'bpo.csv', index=False)

print("DataFrame has been exported to 'output.csv' file.")
