from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

chrome_driver_path = r"C:\Development\chromedriver.exe"
driver = webdriver.Chrome(service=Service(chrome_driver_path))
driver.get("http://orteil.dashnet.org/experiments/cookie/")

parent_element = driver.find_element(By.ID, "store")
upgrade_elements = parent_element.find_elements(By.CSS_SELECTOR, "div b")
item_prices = []

# Convert <b> text into an integer price.
for price in upgrade_elements:
    element_text = price.text
    if element_text != "":
        cost = int(element_text.split("-")[1].strip().replace(",", ""))
        item_prices.append(cost)
print(item_prices)