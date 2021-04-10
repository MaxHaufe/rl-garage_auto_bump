import sys
import argparse
import configparser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep

message = "This is an automatically generated message. Add me on EpicGames: DerMathemann. Only add if you agree to the price in the listing."


def bump_trades(url, email, password, path_to_adblock, path_to_chrome_driver):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    chrome_options.add_argument('load-extension=' + path_to_adblock)

    driver = webdriver.Chrome(path_to_chrome_driver, options=chrome_options)
    # driver.get("http://www.google.com")
    driver.get(url)

    # accept privacy policy
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, 'acceptPrivacyPolicy'))).click()
    # accept privacy policy again (wtf)
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CLASS_NAME, 'css-1tbbj19'))).click()
    # input email
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, 'header-email'))).send_keys(email)
    # input password
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, 'header-password'))).send_keys(password)
    # GO
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.NAME, 'submit'))).click()
    # click on speechbubble if new notifictation, if not time out
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.CLASS_NAME, 'rlg-message-notification.--new'))).click()
    print("new messages found")
    # for each "new" chat do...
    new_chat_list = driver.find_elements_by_class_name('rlg-chat__thread.--is-user.--new.--not-archived')

    for new_chat in new_chat_list:
        new_chat.click()
        sleep(2)
        WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'rlg-input.rlg-chat__input'))).send_keys(message)
        sleep(5)
        WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'fa.fa-paper-plane-o'))).click()


config = configparser.ConfigParser()
config.read("rl_garage.ini")

# todo error handling
email = config["DEFAULT"]["email"]
password = config["DEFAULT"]["password"]
path_to_adblock = config["DEFAULT"]["path_to_adblock"]
path_to_chrome_driver = config["DEFAULT"]["path_to_chrome_driver"]
username = config["DEFAULT"]["username"]

url = "https://rocket-league.com/trades/" + username

bump_trades(url, email, password, path_to_adblock, path_to_chrome_driver)
