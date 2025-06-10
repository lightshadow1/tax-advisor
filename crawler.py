import requests
from bs4 import BeautifulSoup
import certifi
from typing import List, Set

LIMIT = 1
BASE_URL = "https://www.canada.ca"

def find_pdf_links(url: str) -> List[str]:
    """
    Finds PDF links within a website, exploring two levels of depth.

    Args:
        url (str): The base URL of the website to search.

    Returns:
        list: A list of PDF link URLs.
    """

    pdf_links: List[str] = []
    visited_urls: Set[str] = set()

    def crawl(url: str) -> None:
        if url in visited_urls:
            return
        visited_urls.add(url)

        try:
            response = requests.get(url, verify=certifi.where())
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all tables and check the first column for PDF links
            tables = soup.find_all('table')
            for table in tables:
                # print(table)
                rows = table.find_all('tr')
                for row in rows:
                    if not row.find_all('td'):
                        continue
                    columns = row.find_all('td')
                    first_column = columns[0]  # Get only the first column

                    # title = columns[1]
                    update = columns[2]
                    # print(first_column.text, title.text, update.text)
                    # print(first_column.a.get('href'), first_column.text)
                    if '2025' not in update.text:
                        # skip not this year
                        continue
                    print(first_column.a.get('href'), first_column.text)

                    # get links, check if there is a pdf
                    url2 = f"{BASE_URL}{first_column.a.get('href')}"
                    # print(url2)
                    r2 = requests.get(f"{url2}", verify=certifi.where())
                    r2.raise_for_status()  # Raise an exception for HTTP errors
                    s2 = BeautifulSoup(r2.content, 'html.parser')
                    for i in s2.find_all('li'):
                        if 'pdf' in i.text:
                            link2 = i.a.get('href')
                            print(link2)
                            pdf_links.append(link2 + '\n')

        except requests.exceptions.RequestException as e:
            print(f"Error processing {url}: {e}")

    crawl(url)
    return pdf_links

# Example usage
base_url = f"{BASE_URL}/en/revenue-agency/services/forms-publications/publications.html"  # Replace with your desired base URL
pdf_links = find_pdf_links(base_url)
# print(pdf_links)
with open("pdf_links.txt", "w") as f:
    f.writelines(pdf_links)