from selenium import webdriver
from selenium.webdriver.common import keys
import time
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

#E-devlet'ten İstanbul'daki ölüm sayılarını sorgulayan script
#Kullanmak için sselenium'un kurulu olması ve Chrome'un aşağıdaki gibi başlatılması gerekiyor.
#export PATH="/Applications/Google Chrome.app/Contents/MacOS:$PATH"
#Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile" &
#Mecbur olmadıkça Windows kullanmıyorum, o yüzden Windows versiyonunu veremiyorum.

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

driver.get("https://www.turkiye.gov.tr/istanbul-buyuksehir-belediyesi-vefat-sorgulama")

#year = ["2016","2017","2018","2019"]

#Daha önce yılların belirli günlerini sorgulamak için yazmıştım, şimdi tüm yılları sorguluyorum
#o yüzden döngüyü değiştirmedim.
year = ["2008"]

f = open("results_2008_2015.csv","a+")

for i in range(len(year)):
    s = '01/01/'+year[i]
    d = s
    j = 0
    toplam = "0"
    while True:
        driver.find_element_by_id('tarih').clear()
        driver.find_element_by_name('tarih').send_keys(d)
        driver.find_element_by_name('tarih').send_keys(keys.Keys.ENTER)
        try:
            toplam = driver.find_element_by_xpath('//*[@id="contentStart"]/div/div/div/span').get_attribute("innerHTML").split()[1]
        except:
            break

        driver.execute_script("window.history.go(-1)")
        time.sleep(1)
        print(d,toplam,sep = ",")
        f.write(d+","+toplam+"\n")
        j+=1
        if d == "31/12/2015":
            break
        date = datetime.strptime(s, "%d/%m/%Y")
        modified_date = date + timedelta(days=j)
        d = datetime.strftime(modified_date, "%d/%m/%Y")
f.close()
