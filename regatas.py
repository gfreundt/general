import time, json, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as WebDriverOptions
from selenium.webdriver.support.ui import Select
from tqdm import tqdm
import pandas as pd


def set_options():
    options = WebDriverOptions()
    options.add_argument("--window-size=1440,810")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--silent")
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return options


def extract(url, carriles):
    # init driver
    driver = webdriver.Chrome(r"D:\pythonCode\chromedriver.exe", options=set_options())
    # Open webpage in headless Chrome
    driver.get(url)
    # wait 2 sec
    time.sleep(2)
    # fill carnet
    driver.find_element_by_xpath("/html/body/div/div/form/div[1]/input").send_keys(
        "15610"
    )
    # fill password
    driver.find_element_by_xpath("/html/body/div/div/form/div[2]/input").send_keys(
        "Warcraft7"
    )
    # press button iniciar sesion
    driver.find_element_by_xpath("/html/body/div/div/form/div[3]/button").click()
    # wait 3 sec
    time.sleep(2)
    # press button close aviso
    driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[4]/button").click()
    # wait 3 sec
    time.sleep(2)
    # press nueva reserva
    driver.get("https://reservas.regataslima.pe/Reserve/MakeReserve")
    # wait 1 sec
    time.sleep(1)
    # select sede chorrillos
    Select(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div[2]/div/div/div[1]/form/div[1]/div/select"
        )
    ).select_by_value("1")
    # wait 1 sec
    time.sleep(1)
    # select actividad natación (scroll)
    Select(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div[2]/div/div/div[1]/form/div[2]/div/select"
        )
    ).select_by_value("38")
    # wait 1 sec
    time.sleep(1)
    # loop thru select instalacion options
    results = []
    for s in tqdm(carriles):
        Select(
            driver.find_element_by_xpath(
                "/html/body/div[1]/div[3]/div/div/div[2]/div/div/div[1]/form/div[3]/div/select"
            )
        ).select_by_value(s)
        # wait 1 sec
        time.sleep(1)
        # click buscar
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div[2]/div/div/div[1]/form/div[5]/div/button"
        ).click()
        # wait
        time.sleep(0.5)
        results.append({"Carril": s, "Horarios": analyze(driver.page_source)})
    return results


def analyze(text):
    start = text.find("events: [") + 8
    end = text.find("eventClick")
    text = text[start:end]

    response = []
    spos = 0
    while True:
        part1 = text.find("startDate", spos)
        part2 = text.find("reservesAmount", spos)
        if part1 == -1:
            return response
        else:
            spos = part1 + 1

        if text[part2 + 16 : part2 + 17] == "0":
            response.append(
                text[part1 + 12 : part1 + 22] + " @ " + text[part1 + 23 : part1 + 25]
            )


def reorder(data, carriles):
    horarios = [j for i in data for j in i["Horarios"]]
    s = []
    for h in sorted(set(horarios)):
        r = []
        for i in data:
            if h in i["Horarios"]:
                r.append(carriles[i["Carril"]])
        s.append({"Horario": h, "Carriles": sorted(r)})

    # list of dates and start times
    dates = sorted(list(set([i["Horario"][:-5] for i in s])))
    start_times = [f"{i:02d}" for i in range(6, 21)]

    d = []
    for time in start_times:
        t = []
        for date in dates:
            j = ""
            m = date + " @ " + time
            for x in s:
                if m in x["Horario"]:
                    j = x["Carriles"]
            t.append(j)
        d.append(t)

    df = pd.DataFrame(d, columns=dates)
    df.index = start_times

    df.to_excel("output2.xlsx")


def main():
    carriles = {
        "120": "01",
        "157": "10",
        "158": "11",
        "160": "12",
        "161": "13",
        "162": "14",
        "163": "15",
        "164": "16",
        "165": "17",
        "166": "18",
        "167": "19",
        "153": "06",
        "154": "07",
        "155": "08",
        "156": "09",
        "143": "02",
        "144": "03",
        "145": "04",
        "146": "05",
    }

    if "LIVE" in sys.argv:
        r = extract("https://reservas.regataslima.pe/", carriles)
        json_object = json.dumps(r, indent=4)
        with open("output.json", "w") as outfile:
            outfile.write(json_object)
    else:
        with open("output.json", "r") as file:
            r = json.load(file)

    reorder(r, carriles)
    # pd.read_json(json.dumps(s)).to_excel("output.xlsx")


start = time.time()
main()
print(time.time() - start)
