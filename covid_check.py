#TR covid19 data, web scrapper. cansimitus@gmail.com
#This web scrapper extracts daily covid19 data published by TR Ministry of Health
#since it's a web scrapper, it depends of the structure of the web page heavily.
import requests
import re
import sys
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import date

def daily_data():
    #disable any warnings about TLS security
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    URL = 'https://covid19.saglik.gov.tr/'
    page = requests.get(URL, verify=False)

    #ignore any wrongly encoded utf-8 chars, otherwise it's unable to parse the webpage.
    #I had to put this from another scapper, it was unable to decode Turkish Lira symbol in the webpage.
    soup = BeautifulSoup(page.content.decode('utf-8', 'ignore'), 'html.parser')

    #now, the real thing. we look for a div class, and we extract all the items inside it.
    items = soup.find('div', {"class":"corona-bg"}).find_all('li', {"class": re.compile("d-flex justify-content-between baslik-k*")})
    #date is a seperate element on its own, we extract it, format it accordingly, i.e., d.mm.yyyy
    date_dict = {\
    'OCAK':'01',\
    'ŞUBAT':'02',\
    'MART':'03',\
    'NİSAN':'04',\
    'MAYIS':'05',\
    'HAZİRAN':'06',\
    'TEMMUZ':'07',\
    'AĞUSTOS':'08',\
    'EYLÜL':'09',\
    'EKİM':'10',\
    'KASIM':'11',\
    'ARALIK':'12'\
    }
    #the elegance of python. you can combine a loop into a single statementaa
    date = ".".join(date_dict.get(i.text,i.text) for i in soup.find('div', {"class":"takvim text-center"}).find_all('p'))

    #prepare the meta data mapping for the bindings
    tests_dict = {\
    'TOPLAM TEST SAYISI':'tests_total',\
    'TOPLAM VAKA SAYISI':'conf_total',\
    'TOPLAM VEFAT SAYISI':'deaths_total',\
    'TOPLAM YOĞUN BAKIM HASTA SAYISI':'severe_total',\
    'TOPLAM ENTUBE HASTA SAYISI':'intube_total',\
    'TOPLAM İYİLEŞEN HASTA SAYISI':'rec_total',\
    'BUGÜNKÜ TEST SAYISI':'tests_new',\
    'BUGÜNKÜ VAKA SAYISI':'conf_new',\
    'BUGÜNKÜ VEFAT SAYISI':'deaths_new',\
    'BUGÜNKÜ İYİLEŞEN SAYISI':'rec_new'\
    }

    #prepare the dictionary for the data
    data = {\
    'date':'',\
    'conf_new':'',\
    'conf_total':'',\
    'deaths_new':'',\
    'deaths_total':'',\
    'rec_new':'',\
    'rec_total':'',\
    'intube_total':'',\
    'severe_total':'',\
    'tests_new':'',\
    'tests_total':'',\
    'conf_death_rate':'',\
    'active':'',\
    }

    #put the date
    data['date'] = date

    for item in items:
        #the data is placed inside two span tags, first spans[0]->name, second spans[1]->value
        spans = item.find_all('span')

        #extract the name, strip the new line chars (<br>), replace all excess whitespaces with single whitespace
        key = tests_dict[re.sub(' +', ' ',spans[0].text.replace('\n', '').replace('\r', '').strip())]

        #extract the value, place the number without any digit formatting
        value = spans[1].text.strip().replace('.','')

        #push the value to data
        data[key] = value

    data['conf_death_rate'] = str(format(int(data['deaths_total']) / int(data['conf_total'])*100,'.2f'))+"%"
    data['active'] = str(int(data['conf_total']) - (int(data['deaths_total']) + int(data['rec_total'])))

    return data

def main():
    today = date.today().strftime("%-d.%m.%Y")
    with open("covid_tr.csv", "r") as file:
        first_line = file.readline()
        for last_line in file:
            pass
    data = {\
    'date':'',\
    'conf_new':'',\
    'conf_total':'',\
    'deaths_new':'',\
    'deaths_total':'',\
    'rec_new':'',\
    'rec_total':'',\
    'intube_total':'',\
    'severe_total':'',\
    'tests_new':'',\
    'tests_total':'',\
    'conf_death_rate':'',\
    'active':'',\
    }
    data = dict(zip(list(data.keys()),last_line.rstrip().split(',')))

    if data['date'] == today:
        print("Already in file")
        print(\
        data['date'],\
        data['conf_new'],\
        data['conf_total'],\
        data['deaths_new'],\
        data['deaths_total'],\
        data['rec_new'],\
        data['rec_total'],\
        data['intube_total'],\
        data['severe_total'],\
        data['tests_new'],\
        data['tests_total'],\
        data['conf_death_rate'],\
        data['active'],\
        sep=',', end='\n')
        sys.exit()

    data = daily_data()
    if data['date'] == today:
    #print the contents of data in one line, seperated by tab, ended with EOL
        print(\
        data['date'],\
        data['conf_new'],\
        data['conf_total'],\
        data['deaths_new'],\
        data['deaths_total'],\
        data['rec_new'],\
        data['rec_total'],\
        data['intube_total'],\
        data['severe_total'],\
        data['tests_new'],\
        data['tests_total'],\
        data['conf_death_rate'],\
        data['active'],\
        sep=',', end='\n')
    else:
        print("No new data available")
if __name__ == "__main__":
    main()
