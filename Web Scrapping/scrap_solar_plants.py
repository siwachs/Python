import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent


def get_next_page_url(soup, current_page_url):
    links = soup.find_all('a', href=True)
    for link in links:
        if 'pagefrom' in link['href']:
            next_page_url = link['href']
            if next_page_url != current_page_url:
                return next_page_url
    return None


# Initialize UserAgent to mock a device and web browser.
ua = UserAgent()

# Create a session
session = requests.Session()
base_url = "https://www.gem.wiki"
page_url = "/w/index.php?title=Category:Solar_farms_in_India&pagefrom=Rajkot+3+hybrid+solar+farm#mw-pages"
plant_data = []

try:
    while page_url:
        print(page_url)
        time.sleep(3)
        headers = {'User-Agent': ua.random}
        session.headers.update(headers)
        response = session.get(base_url + page_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            category_groups = soup.find_all("div", class_="mw-category-group")

            for category_group in category_groups:
                links = category_group.find_all('ul')[0].find_all('li')
                for link in links:
                    temp_dict = {}
                    link_title = link.find('a').get_text(strip=True)
                    temp_dict['Plant Name'] = link_title
                    link_url = base_url + link.find('a')['href']

                    link_response = session.get(link_url)
                    link_soup = BeautifulSoup(
                        link_response.content, "html.parser")
                    tables = link_soup.find_all("table", class_="wikitable")

                    for table in tables:
                        rows = table.find_all("tr")
                        header_cells = rows[0].find_all("th")
                        header_texts = [header.get_text(
                            strip=True) for header in header_cells]
                        data_dict = {header: [] for header in header_texts}

                        for row in rows[1:]:
                            data_cells = row.find_all("td")
                            data_texts = [data.get_text(strip=True)
                                          for data in data_cells]

                            for header, data_text in zip(header_texts, data_texts):
                                data_dict[header].append(data_text)
                        temp_dict.update(data_dict)

                    plant_data.append(temp_dict)

            # Get the next page URL
            page_url = get_next_page_url(soup, page_url)

        else:
            print(
                f"Failed to retrieve the page. Status code: {response.status_code}")
            break
except Exception as e:
    print(e)

df = pd.DataFrame(plant_data)
df.to_excel("plant_data.xlsx", index=False)
print("DataFrame saved to plant_data.xlsx")
