import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of nutrients and their corresponding URLs
nutrients = {
    "iron": "https://tools.myfooddata.com/nutrient-ranking-tool/iron/beans-and-lentils+dairy-and-egg-products+fish+fruits+grains-and-pasta+meats+nuts-and-seeds+spices-and-herbs+vegetables/highest/grams/sr/no",
    "folate-b9": "https://tools.myfooddata.com/nutrient-ranking-tool/folate-b9/beans-and-lentils+dairy-and-egg-products+fish+fruits+grains-and-pasta+meats+nuts-and-seeds+spices-and-herbs+vegetables/highest/grams/sr/no",
    "vitamin-b12": "https://tools.myfooddata.com/nutrient-ranking-tool/vitamin-b12/beans-and-lentils+dairy-and-egg-products+fish+fruits+grains-and-pasta+meats+nuts-and-seeds+spices-and-herbs+vegetables/highest/grams/sr/no",
}

# Function to scrape one table
def scrape_table(url, nutrient):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")[0:201]  # Skip header, get top 200

    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue
        # Extract fields based on class names and structure
        rank = cols[1].get_text(strip=True)
        food_name = cols[2].find("span", class_="searchTable__fullName")
        food_name = food_name.get_text(strip=True) if food_name else ""
        serving = cols[2].find("span", class_="searchTable__serving")
        serving = serving.get_text(strip=True) if serving else ""
        nutrient_val = cols[3].find("span", class_="searchTable")
        nutrient_val = nutrient_val.get_text(strip=True) if nutrient_val else ""
        percent_dv = cols[3].find("span", class_="searchTable__percentage")
        percent_dv = percent_dv.get_text(strip=True) if percent_dv else ""
        source = cols[4].find("span", class_="searchTable__sourceName")
        source = source.get_text(strip=True) if source else ""

        data.append({
            "Rank": rank,
            "Food Name": food_name,
            "Serving": serving,
            f"{nutrient} amount": nutrient_val,
            "Percent DV": percent_dv,
            "Source": source
        })

    return pd.DataFrame(data)

# Scrape all three nutrients into separate DataFrames
dfs = {}
for nutrient, url in nutrients.items():
    dfs[nutrient] = scrape_table(url, nutrient)

# Example: Save each DataFrame as CSV
dfs["iron"].to_csv("top_200_iron.csv", index=False)
dfs["folate-b9"].to_csv("top_200_folate_b9.csv", index=False)
dfs["vitamin-b12"].to_csv("top_200_vitamin_b12.csv", index=False)
