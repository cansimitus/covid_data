from selenium import webdriver
from selenium.webdriver.common import keys
import time
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import sys
import os

def process_args():
    global start_date, end_date, filename
    start_date = ""
    end_date = ""
    filename = ""

    if len(sys.argv) < 4:
        print("Usage: "+sys.argv[0]+" start_date[format=dd/mm/yyyy] end_date[format=dd/mm/yyyy] filename")
        sys.exit()

    start_date = sys.argv[1]
    end_date   = sys.argv[2]
    filename   = sys.argv[3]

    if datetime.strptime(start_date, "%d/%m/%Y") > datetime.strptime(end_date, "%d/%m/%Y"):
        print("start_date>end_date! Exiting")
        sys.exit()

def get_next_day(day):
    date = datetime.strptime(day, "%d/%m/%Y")
    modified_date = date + timedelta(days=1)
    return datetime.strftime(modified_date, "%d/%m/%Y")

if __name__ == "__main__":
    process_args()
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)

    driver.get("https://www.turkiye.gov.tr/istanbul-buyuksehir-belediyesi-vefat-sorgulama")
    f = open(filename,"a+")
    current_date = start_date
    j = 0
    deaths = "0"
    while True:
        driver.find_element_by_id('tarih').clear()
        driver.find_element_by_name('tarih').send_keys(current_date)
        driver.find_element_by_name('tarih').send_keys(keys.Keys.ENTER)
        try:
            deaths = driver.find_element_by_xpath('//*[@id="contentStart"]/div/div/div/span').get_attribute("innerHTML").split()[1]
        except:
            break
        driver.execute_script("window.history.go(-1)")
        time.sleep(1)
        print(current_date,deaths,sep = ",")
        f.write(current_date+","+deaths+"\n")
        if current_date == end_date:
            break
        j+=1
        current_date = get_next_day(current_date)
    f.close()
