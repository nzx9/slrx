import secrets
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import os
import dotenv
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

driver = webdriver.Chrome()


driver.get("https://dscapp.herokuapp.com/accounts/login")

driver.implicitly_wait(0.5)

# # login as admin
admin_username_field = driver.find_element(by=By.NAME, value="username")
admin_password_field = driver.find_element(by=By.NAME, value="password")
admin_submit_button = driver.find_element(by=By.CSS_SELECTOR, value=".submit")


admin_username_field.send_keys(os.environ.get("ADMIN_USERNAME"))
admin_password_field.send_keys(os.environ.get("ADMIN_PASSWORD"))
admin_submit_button.click()

driver.implicitly_wait(1000)

driver.get("https://dscapp.herokuapp.com/admin/auth/user/add/")

driver.implicitly_wait(1000)


with open(os.path.join(BASE_DIR, "secrets", "accounts.txt")) as f:
    accounts = f.readlines()

    for account in accounts:
        username, password = account.split("\t")
        driver.find_element(by=By.NAME, value="username").send_keys(username)
        # time.sleep(2)
        driver.find_element(by=By.NAME, value="password1").send_keys(password)
        # time.sleep(2)
        driver.find_element(by=By.NAME, value="password2").send_keys(password)
        time.sleep(10)
        driver.find_element(by=By.NAME, value="_addanother").click()
        time.sleep(2)
        driver.find_element(by=By.NAME, value="username").clear()
        driver.find_element(by=By.NAME, value="password1").clear()
        driver.find_element(by=By.NAME, value="password2").clear()
        time.sleep(10)
