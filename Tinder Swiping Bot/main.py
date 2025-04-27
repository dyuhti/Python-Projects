from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

EMAIL = "***"
PASSWORD = "***"

chrome_driver_path = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=chrome_driver_path)
driver.get("https://tinder.onelink.me/***/****")

base_window = driver.current_window_handle
time.sleep(4)

# FaceBook login-click
try:
    facebook_login = driver.find_element(By.XPATH,
                                         '/html/body/div[2]/main/div[1]/div/div[1]/div/div/div[2]/div[2]/span/div[2]/button').click()
    time.sleep(5)
except:
    more_options = driver.find_element(By.XPATH,
                                       '/html/body/div[2]/main/div[1]/div/div[1]/div/div/div[2]/div[2]/span/button').click()
    time.sleep(5)


window_handle_list = driver.window_handles
driver.switch_to.window(window_handle_list[1])

# FaceBook email entry
input_email = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/form/div/div[1]/div/input")
input_email.send_keys(EMAIL)
time.sleep(5)

# FaceBook password entry
password = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/form/div/div[2]/div/input')
password.send_keys(PASSWORD)
time.sleep(5)

# Click-login
login = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]').click()
time.sleep(10)


driver.switch_to.window(base_window)
print(driver.title)

time.sleep(8)

location = driver.find_element(By.XPATH, value='/html/body/div[2]/main/div/div/div/div[3]/button[1]')

location.click()

time.sleep(15)

notification = driver.find_element(By.XPATH, value='/html/body/div[2]/main/div/div/div/div[3]/button[2]')

notification.click()

time.sleep(15)

night_mode = driver.find_element(By.XPATH, value='/html/body/div[2]/main/div/div[2]/button')

night_mode.click()
time.sleep(10)

while True:
# Dislike
    try:
        dislike_button = driver.find_element(By.XPATH, value="/html/body/div[1]/div/div[1]/div/div/main/div/div/div[1]/div/div[3]/div/div[2]/button").click()
        time.sleep(2)

    except ElementClickInterceptedException:
        not_interested_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/main/div/div[2]/button[2]')
        not_interested_button.click()
        time.sleep(3)
