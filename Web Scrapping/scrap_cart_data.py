from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = 'https://magicpin.in/New-Delhi/Paharganj/Restaurant/Eatfit/store/61a193/delivery'

driver = webdriver.Firefox()
driver.get(url)

try:
    while True:
        # Wait for the main container to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'order-summary-details')))

        # Get the current price data
        try:
            current_price_element = driver.find_element(
                By.CLASS_NAME, 'finalPrice')
            current_price = current_price_element.text
            print(f"Current Price: {current_price}")
        except Exception as e:
            print("Current Price: 0")

        # Check if the cart is empty
        try:
            empty_cart = driver.find_element(
                By.CLASS_NAME, 'empty-cart').is_displayed()
            print("Cart is empty")
        except Exception as e:
            pass

        time.sleep(3)  # Wait for 3 seconds before checking again

except Exception as e:
    print(f"An error occurred: {str(e)}")
