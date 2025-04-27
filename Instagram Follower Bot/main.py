import time
from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

CHROME_DIVER_PATH = "C:\Development\chromedriver.exe"
SIMILAR_ACCOUNT = "chefsteps"
USERNAME = "pythonlearner962"
PASSWORD = "5)'2ZAW)QiTyD$M"


class InstaFollower:
    def __init__(self):
        self.chrome_driver_path = Service(CHROME_DIVER_PATH)
        self.driver = webdriver.Chrome(service=self.chrome_driver_path)
        self.driver.get("https://www.instagram.com")
        time.sleep(7)

    def login(self):
        self.username_login = self.driver.find_element(By.XPATH,
                                                       value="/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input")
        self.username_login.send_keys(USERNAME)
        time.sleep(5)
        self.password_login = self.driver.find_element(By.XPATH,
                                                       value="/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")
        self.password_login.send_keys(PASSWORD)
        time.sleep(5)
        self.login_button = self.driver.find_element(By.XPATH,
                                                     value="/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button").click()
        time.sleep(5)

    def find_followers(self):
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}")
        time.sleep(10)
        self.followers = self.driver.find_element(By.XPATH,
                                                  value="/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(10)
        self.popup = self.driver.find_element(By.XPATH,
                                              value="/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")
        time.sleep(7)
        # for i in range(100):
        #     self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", self.popup)
        #     time.sleep(2)

    def follow(self):
        self.all_follow_button = self.driver.find_element(By.XPATH,
                                 value="/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div/div[3]/div/button")
        while True:
            try:
                self.all_follow_button .click()
                time.sleep(2)
            except ElementClickInterceptedException:
                self.driver.find_element(By.XPATH, value="/html/body/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/button[2]")



bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()
bot.driver.quit()
