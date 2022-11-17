from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def getConversationIds(browserLocation, email, passwd, out_file):
    data = []
    browser = webdriver.Firefox(browserLocation)
    browser.get("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")
    time.sleep(2)
    username = browser.find_element(By.ID, "username")
    username.send_keys(email)

    password = browser.find_element(By.ID, "password")
    password.send_keys(passwd)

    # click on login button
    browser.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)

    # click on the messages
    message_btn = browser.find_element(
        By.XPATH, "/html/body/div[6]/header/div/nav/ul/li[4]/a"
    )
    if message_btn:
        # click on it
        message_btn.click()
        time.sleep(1)
        my_xpath = WebDriverWait(browser, 40).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[6]/div[3]/div[2]/div/div/main/div/section[1]/div[2]/ul",
                )
            )
        )
        start = time.time()
        init = 0
        step = 400
        while True:
            browser.execute_script(f"arguments[0].scroll({init},{step})", my_xpath)
            time.sleep(2)
            init = step
            step += 500
            end = time.time()
            # We will scroll for 5 seconds.
            if round(end - start) > 10:
                break
        time.sleep(3)

        source = browser.page_source
        soup = BeautifulSoup(source, "lxml")

        conversation_ids = soup.find_all(
            "a", {"class": "msg-conversation-listitem__link"}
        )
        if conversation_ids:
            for conv in conversation_ids:
                data.append(conv["href"])
        # save the file as csv
        pd.DataFrame(data, columns=["ID"]).drop_duplicates().to_csv(
            out_file, index=False
        )

        browser.close()
