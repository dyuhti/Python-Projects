import time

from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
GOOGLE_FORM = "https://docs.google.com/forms/****"
ZILLOW = "https://www.zillow.com/san-francisco-ca/rentals/****"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
    "Accept-Language": "en-US"
}


class RentingWebsite:
    def __init__(self):
        self.response = requests.get(ZILLOW, headers=headers)
        self.web_page = self.response.text
        self.soup = BeautifulSoup(self.web_page, "html.parser")
        self.chrome_driver_path = Service(CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=self.chrome_driver_path)
        self.driver.get(GOOGLE_FORM)
        self.price_list = []
        self.address_list = []
        self.links_list = []
        self.listing_links = []

    def zillow_webscraping(self):

        # Prices of apartment
        self.prices = self.soup.find_all('span', attrs={'data-test': 'property-card-price'})
        for price in self.prices:
            price_text = str(price).strip(
                'PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr" data-test="property-card-price"><span class="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr" data-test="property-card-price">+ 1 bd</jLQjry" data-test="property-card-price">')
            self.price_list.append(price_text)
        # print(self.price_list)

        # Listing Address
        self.all_listing_address = self.soup.find_all('address', attrs={'data-test': 'property-card-addr'})
        for address in self.all_listing_address:
            address_text = str(address).strip('<address data-test="property-card-addr"></address>')
            self.address_list.append(address_text)
        # print(self.address_list)

        # Listing link
        for duplicate_link in self.soup.find_all('a', attrs={"data-test": "property-card-link"}, href=True):
            link_ = duplicate_link['href']
            removed_elements = str(link_).strip("https://www.zillow.com")
            if removed_elements not in self.links_list:
                self.links_list.append(removed_elements)
        self.listing_links = ['https://www.zillow.com/' + link for link in self.links_list]
        print(self.listing_links)

    def enter_in_google_sheet(self):

        # Loop through the all the list using same indices
        for each_index in range(8):
            # # Enter address of property
            self.enter_address = self.driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            self.enter_address.send_keys(self.address_list[each_index])
            time.sleep(5)

            # Price
            self.enter_price = self.driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            self.enter_price.send_keys(self.price_list[each_index])
            time.sleep(5)

            # Link to property
            self.enter_link = self.driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            self.enter_link.send_keys(self.listing_links[each_index])
            time.sleep(10)

            # Submit button
            self.submit_button = self.driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            self.submit_button.click()

            # Submit another response
            self.submit_another_response = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            self.submit_another_response.click()

bot = RentingWebsite()
bot.zillow_webscraping()
bot.enter_in_google_sheet()


