import pandas as pd
from scape import BeautifulSoup

# Sample HTML content
with open("school.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract records
records = []
for listing in soup.find_all(class_="search-listing"):
    business_name = listing.find(class_="search-business-name").text.strip()
    # capsule_rounded = listing.find(class_="search-capsule-rounded").text.strip()
    address = listing.find(class_="search-busines-address").text.strip()
    phone_element = listing.find("a", class_="btn btn-yp-default mr-2 yp-click")
    phone = phone_element.get("href") if phone_element else None
    records.append((business_name, address, phone))

# Create DataFrame
df = pd.DataFrame(records, columns=["Business Name", "Address", "Phone"])

# Save DataFrame to CSV
df.to_csv("schools.csv", index=False)

print("CSV file saved successfully.")

# https://www.yellow-pages.ph/category/schools/page-10
# RegEx: ^\s*$\n - to remove black rows spaces