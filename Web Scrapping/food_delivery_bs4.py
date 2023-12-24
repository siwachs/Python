from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


def get_loaded_menu(menu):
    try:
        h4_title = article.find('h4', class_='categoryHeading')
        div = article.find('div')
        category_item_holder_list = div.find_all(
            'section', class_='categoryItemHolder')
        for category_item_holder in category_item_holder_list:
            item_details = category_item_holder.find(
                'div', class_='itemDetails')
            item_details_article = item_details.find(
                'article', class_='itemInfo')
            p_tags = item_details_article.find_all('p')

            # Check if at least two p tags exist for menu title and price
            if len(p_tags) >= 2:
                item_name_element = p_tags[0]
                item_price_element = p_tags[1]
                item_name_element_link = item_name_element.find('a')
                item_name = item_name_element_link.text.strip()
                item_price_element_span = item_price_element.find('span')
                item_price = item_price_element_span.text.strip()

                # Add item to the menu dictionary
                if h4_title.text.strip() in menu:
                    menu[h4_title.text.strip()].append({item_name: item_price})
                else:
                    menu[h4_title.text.strip()] = [{item_name: item_price}]
    except Exception as e:
        print(f"Error: {e}")


try:
    # Set up the browser
    driver = webdriver.Firefox()
    url = 'https://magicpin.in/New-Delhi/Paharganj/Restaurant/Eatfit/store/61a193/delivery'
    driver.get(url)

    # Allow some time for the page to load dynamically
    time.sleep(1)  # Adjust the sleep duration based on the page load time

    # Find and store all arrow-down icons in a list
    arrow_down_icons = driver.find_elements(By.CLASS_NAME, 'minimiseIcon')
    expanded_page_sources = []
    for arrow_down in arrow_down_icons:
        arrow_down.click()
        time.sleep(1)

    # Get the page source after dynamic content is loaded
    page_source = driver.page_source

    # Quit the Selenium driver as we have obtained the required page source
    driver.quit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract the menu information
    menu = {}
    catalog = soup.find('div', class_='catalogItemsHolder')
    articles = catalog.find_all('article')

    for article in articles:
        try:
            get_loaded_menu(menu)

        except Exception as e:
            print(f"Error inside article loop: {e}")

    # Print the menu
    print("Menu:")
    for category, items in menu.items():
        print(f"\n{category}:")
        for item in items:
            for item_name, item_price in item.items():
                print(f"{item_name}: {item_price}")

except Exception as e:
    print(f"Error outside article loop: {e}")
