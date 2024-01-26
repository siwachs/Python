from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL and web driver setup
base_url = "https://www.gem.wiki"
page_url = "/w/index.php?title=Category:Solar_farms_in_India&pageuntil=Gale+%28UPC%29+solar+farm#mw-pages"

options = webdriver.FirefoxOptions()
options.headless = True  # Run the browser in headless mode (without GUI)
driver = webdriver.Firefox(options=options)

# Create an empty list to store data
plant_data = []

try:
    def get_next_page_url(soup, current_page_url):
        links = soup.find_all('a', href=True)
        for link in links:
            if 'pagefrom' in link['href']:
                next_page_url = link['href']
                if next_page_url != current_page_url:
                    return next_page_url
        return None

    while page_url:
        print(base_url+page_url)

        # Open the page
        driver.get(base_url+page_url)
        time.sleep(3)

        # Extract data using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        category_groups = soup.find_all("div", class_="mw-category-group")

        for category_group in category_groups:
            links = category_group.find_all('ul')[0].find_all('li')
            for link in links:
                temp_dict = {}
                link_title = link.find('a').get_text(strip=True)
                temp_dict['Plant Name'] = link_title
                link_url = base_url + link.find('a')['href']

                # Extract data from the linked page
                driver.get(link_url)
                link_soup = BeautifulSoup(driver.page_source, "html.parser")
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
        driver.get(base_url+page_url)
        time.sleep(3)
        page_url = get_next_page_url(soup, page_url)

except Exception as e:
    print(e)

finally:
    # Close the browser window
    driver.quit()

# Convert the data to a DataFrame and save it to an Excel file
df = pd.DataFrame(plant_data)
df.to_excel("plant_data_selenium.xlsx", index=False)
print("DataFrame saved to plant_data_selenium.xlsx")
