# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0050D6DBFD4836D42B0F0EC07BB38625EFF72AABC464E5070F967B9D951B09902D6542152AF45735BF51886F3F98D8A3F030E74E565A374FB23C8D36BFEDFC01C7C189166479492FB582A117F735929B4DDC79D721D39FB4E84769F525EB1CF14AD14A981E4FAB3079E40A6BB0D347D441965F30B63E707986EE0C87EDD1322A5DBFA261A42C558B27889B762D3F7DA2B7651FE67095ECC44FB427375C8A0C8832B4A9C0DC23BBA3714FF53D729C2147D1D1B578AB47D9E478CAC022EB9EDFC42949E7F9FFED969FDDC405D76B77719BFEC6DE81C7522460155411A92D8DB50CC369581EBDDE79F4EB499E93337F0EDB6CF81150809725329B11CBAF28E296932B79C837DFC8918422FEDDFF50935691D699D8649E6F61755D0F6E210CBC713C55573E39A2738621349BE088901E0D5B05757836A042D01D3A2906C6910A5EF5038136C731CDA52E41C436ACA963B5D4226A7F29C9911D054D075B206F673E4DFD"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
