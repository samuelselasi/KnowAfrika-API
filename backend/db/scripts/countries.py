#!/usr/bin/env python3
"""Script that scrapes country and province info from wikipedia"""
import requests
import csv


def get_african_countries():
    """Define the Wikipedia API URL for a list of African countries"""

    url = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:Countries_in_Africa"

    response = requests.get(url)
    data = response.json()

    # Extracting country titles from the API response
    country_titles = [entry['title'] for entry in data[
        'query']['categorymembers']]

    return country_titles


def get_regions_provinces(country):
    """Define the Wikipedia API URL for a country's regions/provinces"""

    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={country}&rvprop=content"

    response = requests.get(url)
    data = response.json()

    # Extracting information about regions/provinces from the API response
    pages = data['query']['pages']
    regions_provinces = []
    for page_id, page_info in pages.items():
        content = page_info['revisions'][0]['*']
        # Modify the extraction logic based on the actual structure of page
        # You might want to use regular expressions or other techniques
        # to extract the relevant information from the page content
        regions_provinces.append(content)

    return regions_provinces


def scrape_african_countries():
    country_titles = get_african_countries()

    with open('countries_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['Country', 'Region/Province']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for country in country_titles:
            regions_provinces = get_regions_provinces(country)

            # Write data to CSV file
            writer.writerow({'Country': country, 'Region/Province': ', '.join(
                regions_provinces)})

    print("Scraping completed. Data saved to 'countries_data.csv'")


if __name__ == "__main__":
    scrape_african_countries()
