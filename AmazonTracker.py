import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

# the product's URL
product_URL = 'https://www.amazon.com/Apple-MacBook-15-inch-2-3GHz-8-core/dp/B07S58MHXF'

# define user agent
header_agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

# track current price and lowest historical price
current_price = None
hist_lowest_price = current_price

def check_price(hist_lowest_price, current_price):
    page = requests.get(product_URL, headers=header_agent) # go to URL
    soup = BeautifulSoup(page.content, 'html.parser') # parse URL content

    title = soup.find(id='productTitle').get_text().strip() # find product title
    title = title[:25] + "..." # truncate product title
    price = soup.find(id='priceblock_ourprice').get_text() # find product price
    price = price.replace(',', '') # format for float conversion
    current_price = float(price[1:]) # convert product price to int, record current known price

    print(f"[{get_time()}] Monitoring price of: {title}")
    print(f"[{get_time()}] Current Price: ${current_price}\n")

    # if historical lowest not set, set it!
    if hist_lowest_price is None:
        hist_lowest_price = current_price
    elif current_price < hist_lowest_price: # check if price dropped compared to hist_low
        print(f"Price has dropped for {title}!")
        print(f"Old Price: ${hist_lowest_price}")
        print(f"New price: ${current_price}")
        print(f"Change: ${(hist_lowest_price - current_price)}\n")
        hist_lowest_price = current_price

def get_time():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

# run forever :)
while(True):
    check_price(hist_lowest_price, current_price)
    time.sleep(5 * 60)
