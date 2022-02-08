import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as WebDriverOptions
from selenium.webdriver.support.ui import Select
from datetime import datetime as dt
import easyocr
import yagmail


def set_options():
    options = WebDriverOptions()
    # options.add_argument("--start-maximized")
    options.add_argument("--window-size=2560,1440")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--silent")
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return options


def navigate(url, img):
    # init driver
    driver = webdriver.Chrome(r"D:\pythonCode\chromedriver.exe", options=set_options())

    # Open webpage in headless Chrome
    driver.get(url)
    time.sleep(2)

    # press lupa
    driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[1]/div[1]/div[1]/form/table[1]/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/a/img"
    ).click()
    time.sleep(2)

    # fill "san isidro" to start search
    driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[1]/div[1]/div[1]/form/div[4]/div[2]/table[1]/tbody/tr[1]/td[2]/input"
    ).send_keys("san isidro")
    time.sleep(2)

    # press buscar
    driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[1]/div[1]/div[1]/form/div[4]/div[2]/table[1]/tbody/tr[4]/td[1]/button/span[2]"
    ).click()
    time.sleep(2)

    # select MSI
    driver.find_element_by_link_text(
        "MUNICIPALIDAD DISTRITAL DE SAN ISIDRO - LIMA"
    ).click()
    time.sleep(2)

    # select 2021 (no idea why I need to put 2019 but it works)
    driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[1]/div[1]/div[1]/form/table[1]/tbody/tr[1]/td/table/tbody/tr[3]/td[4]/div/div[2]/input"
    ).send_keys("2019")
    time.sleep(2)

    # get captcha and input in box
    pass_captcha(driver)
    time.sleep(2)

    # select ficha
    driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[1]/div[1]/div[1]/form/table[2]/tbody/tr/td/div/div[2]/div/div[1]/table/tbody/tr[11]/td[13]/a[2]/img"
    ).click()
    time.sleep(2)
    # screenshot 1 saved
    driver.save_screenshot(img[0])
    time.sleep(2)

    # select
    driver.find_element_by_xpath(
        "/html/body/div[3]/div/div/div/div/form/fieldset[3]/div/table/tbody/tr[1]/td[3]/a/img"
    ).click()
    time.sleep(2)
    # screenshot 2 saved
    driver.save_screenshot(img[1])

    time.sleep(10)


def pass_captcha(driver):
    while True:  # loops until captcha has been accepted by webpage
        captcha_format = False
        while not captcha_format:
            # download image
            with open("captcha.jpg", "wb") as file:
                file.write(
                    driver.find_element_by_xpath(
                        "/html/body/div[3]/div/div[1]/div[1]/div[1]/form/table[1]/tbody/tr[5]/td/table/tbody/tr/td[2]/img[2]"
                    ).screenshot_as_png
                )
            time.sleep(1)
            # process image
            captcha = easyocr.Reader(["en"]).readtext("captcha.jpg")[0][1]
            if len(captcha) == 5:
                captcha_format = True
            else:
                # refresh captcha
                driver.find_element_by_xpath(
                    "/html/body/div[3]/div/div[1]/div[1]/div[1]/form/table[1]/tbody/tr[5]/td/table/tbody/tr/td[2]/button/span[1]"
                ).click()
                time.sleep(2)

        # enter image in box
        driver.find_element_by_xpath(
            "/html/body/div[3]/div/div[1]/div[1]/div[1]/form/table[1]/tbody/tr[5]/td/table/tbody/tr/td[2]/input"
        ).send_keys(captcha)
        time.sleep(2)

        # click buscar
        driver.find_element_by_xpath(
            "/html/body/div[3]/div/div[1]/div[1]/div[1]/form/table[1]/tfoot/tr/td/div/button[1]/span[2]"
        ).click()
        time.sleep(2)

        if driver.find_elements_by_xpath(
            "/html/body/div[3]/div/div[1]/div[1]/div[1]/form/table[2]/tbody/tr/td/div/div[2]/div/div[1]/table/tbody/tr[7]/td[13]/a[2]/img"
        ):
            return

        time.sleep(2)


def send_gmail(attach):
    sender = "gfreundt@gmail.com"
    send_to_list = ["gfreundt@losportales.com.pe"]
    subject = "Estado SEACE " + dt.now().strftime("%m-%d-%Y  %H-%M")
    body = "Actualizado."
    yag = yagmail.SMTP(sender)
    for to in send_to_list:
        yag.send(to=to, subject=subject, contents=body, attachments=attach)


def main():
    start = time.time()
    url = "https://prodapp2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml"
    image_list = [
        f"SEACE-PRINCIPAL {dt.now().strftime('%m-%d-%Y  %H-%M')}.png",
        f"SEACE-ACCIONES {dt.now().strftime('%m-%d-%Y  %H-%M')}.png",
    ]
    navigate(url, image_list)
    send_gmail(image_list)
    print(f"Total time: {time.time() - start}")


# main()

send_gmail(
    ["SEACE-ACCIONES 02-08-2022  15-43.png", "SEACE-PRINCIPAL 02-08-2022  15-43.png"]
)