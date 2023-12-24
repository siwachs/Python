import requests
from bs4 import BeautifulSoup
import pandas as pd

Item_name = []
Item_price = []

url = "https://magicpin.in/New-Delhi/Paharganj/Restaurant/Eatfit/store/61a193/delivery"

webpage = requests.get(url)

soup = BeautifulSoup(webpage.text, "lxml")

table = soup.find_all("div", class_="catalogItemsHolder")

name = soup.find_all("a", class_="itemName")
price = soup.find_all("span", class_="itemPrice")

for i in name:
    name = i.text
    Item_name.append(name)

for j in price:
    price = j.text
    Item_price.append(price)

df = pd.DataFrame({"Item Name": Item_name, "Price": Item_price})
df.to_excel('result.xlsx', index=False)
