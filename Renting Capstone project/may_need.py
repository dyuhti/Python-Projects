
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
ZILLOW = "https://www.zillow.com/san-francisco-ca/rentals/****"

CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
chrome_driver_path = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=chrome_driver_path)
driver.get(ZILLOW)


