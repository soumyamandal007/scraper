from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import environ
from selenium.webdriver import Remote, ChromeOptions as Options
from selenium.webdriver.common.action_chains import ActionChains 
import csv
import os
import hashlib


PATH = "/Users/soumya/Desktop/practice/selenium/chromedriver-mac-x64/chromedriver"

service = Service(PATH)
options = Options()
options.add_argument("--no-sandbox")
options.add_argument('disable-notifications')
driver = webdriver.Chrome(service = service, options = options)


#discarding the cookie button
# try:
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))).click()
#     print('declined cookies')
# except Exception as e:
#     print('no cookie button!')
# time.sleep(2)

def scrape_products():
    items = driver.find_elements(By.CLASS_NAME,'s-item__wrapper')
    for item in items:
        try:
            title = item.find_element(By.CLASS_NAME, 's-item__title').text
            price = item.find_element(By.CLASS_NAME, 's-item__price').text
            product_link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            image_link = item.find_element(By.CSS_SELECTOR,'img').get_attribute('src')
            item_id = int(hashlib.md5(product_link.encode('utf-8')).hexdigest(), 16)
            writer.writerow([item_id, title if title else 'N/A', price if price else 'N/A', image_link, product_link])
            print(f'Added file to csv: {item_id}')
        except Exception as e:
            print("Problemss ")
            continue
        

# # Path to your CSV file
file_path = 'ebay_products11.csv'  

keys = ["Women Clothing", "Men Clothing"]
action = ActionChains(driver)

with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Item ID', 'Name', 'Price', 'Image Link', 'Product Link'])

for k in keys:
    driver.get("https://www.ebay.com/")
    print(driver.title)
    driver.maximize_window()
    searchBar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ui-autocomplete-input")))
    action.click(searchBar).perform()
    searchBar.clear()
    action.send_keys(k).perform()
    action.send_keys(Keys.RETURN).perform()

    time.sleep(2)

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        i = 1
        while i < 2:
            scrape_products()
            try:
                next_button = driver.find_element(By.CLASS_NAME, 'pagination__next')
                next_button.click()
                i += 1
                print(f"Page Completed---{i}")
                time.sleep(3)
            except Exception as e:
                print("No more pages to scrape")
                break

        