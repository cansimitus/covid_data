from selenium import webdriver
from selenium.webdriver.common import keys
import time
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

#E-devlet'ten İstanbul'daki ölüm sayılarını sorgulayan script
#Kullanmak için sselenium'un kurulu olması ve Chrome'un aşağıdaki gibi başlatılması gerekiyor.
#export PATH="/Applications/Google Chrome.app/Contents/MacOS:$PATH"
#Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile" &
#Mac/Linux Kullanmayan developer olamaz, o yüzden Windows versiyonunu veremiyorum.

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

year = ["2016","2017","2018","2019","2020"]
for i in range(5):
    s = '01/03/'+year[i]
    for j in range(41):
        time.sleep(3)
        date = datetime.strptime(s, "%d/%m/%Y")
        modified_date = date + timedelta(days=j)
        d = datetime.strftime(modified_date, "%d/%m/%Y")
        driver.find_element_by_id('tarih').clear()
        driver.find_element_by_name('tarih').send_keys(d)
        driver.find_element_by_name('tarih').send_keys(keys.Keys.ENTER)
        toplam = driver.find_element_by_xpath('//*[@id="contentStart"]/div/div/div/span').get_attribute("innerHTML").split()
        print(d,toplam[1],sep=",")
        driver.execute_script("window.history.go(-1)")
