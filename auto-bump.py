import configparser
import os
import argparse


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep

# cmdline args
parser = argparse.ArgumentParser(description="Options for bömping")
parser.add_argument("--debug", dest="debug", action="store_true", help="debug prints")
args = parser.parse_args()

def bump_trades(url, email, password, path_to_chrome_driver):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])

    driver = webdriver.Chrome(path_to_chrome_driver, options=chrome_options)
    driver.get(url)

    if args.debug:
        print("Get request done")
    # accept privacy policy
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, 'acceptPrivacyPolicy'))).click()
    if args.debug:
        print("clicked privacy I")
    # accept privacy policy again (wtf)
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CLASS_NAME, 'css-1tbbj19'))).click()
    if args.debug:
        print("clicked privacy II")
    # input email
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, 'header-email'))).send_keys(email)
    if args.debug:
        print("input email done")
    # input password
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, 'header-password'))).send_keys(password)
    if args.debug:
        print("input password done")
    # GO
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.NAME, 'submit'))).click()
    if args.debug:
        print("submit clicked")
    # todo exception handling
    # no button exists, trade was already bömped
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.CLASS_NAME, 'rlg-trade__action.rlg-trade__bump.--bump')))

    bump_button_list = driver.find_elements_by_class_name('rlg-trade__action.rlg-trade__bump.--bump')
    if args.debug:
        print("found " + str(len(bump_button_list)) + " trades")

    for count, bump_button in enumerate(bump_button_list):
        bump_button.click()
        sleep(2)  # idk if that is necessary
        WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/span/i'))).click()
        if args.debug:
            print("clicked trade nr " + str(count+1))


def main():
    config = configparser.ConfigParser()
    path_to_config = os.path.dirname(os.path.abspath(__file__)) + "/rl_garage.ini"
    config.read(path_to_config)

    # todo error handling
    email = config["DEFAULT"]["email"]
    password = config["DEFAULT"]["password"]
    path_to_chrome_driver = config["DEFAULT"]["path_to_chrome_driver"]
    username = config["DEFAULT"]["username"]

    url = "https://rocket-league.com/trades/" + username

    bump_trades(url, email, password, path_to_chrome_driver)


if __name__ == "__main__":
    main()
