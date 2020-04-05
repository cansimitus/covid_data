#TR covid19 data, web scrapper. cansimitus@gmail.com
#This web scrapper extracts daily covid19 data published by TR Ministry of Health
#since it's a web scrapper, it depends of the structure of the web page heavily.
import requests
import re
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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

date = ".".join(i.text for i in soup.find('div', {"class":"takvim text-center"}).find_all('p'))
mapping = [\
('OCAK', '01'),\
('ŞUBAT', '02'),\
('MART', '03'),\
('NİSAN', '04'),\
('MAYIS', '05'),\
('HAZİRAN', '06'),\
('TEMMUZ', '07'),\
('AĞUSTOS', '08'),\
('EYLÜL', '09'),\
('EKİM', '10'),\
('KASIM', '11'),\
('ARALIK', '12')\
]
for k, v in mapping:
    date = date.replace(k, v)

#prepare the meta data mapping for the bindings
mapping2 = [\
('TOPLAM TEST SAYISI','tests_total'),\
('TOPLAM VAKA SAYISI','conf_total'),\
('TOPLAM VEFAT SAYISI','deaths_total'),\
('TOPLAM YOĞUN BAKIM HASTA SAYISI','severe_total'),\
('TOPLAM ENTUBE HASTA SAYISI','intube_total'),\
('TOPLAM İYİLEŞEN HASTA SAYISI','rec_total'),\
('BUGÜNKÜ TEST SAYISI','tests_new'),\
('BUGÜNKÜ VAKA SAYISI', 'conf_new'),\
('BUGÜNKÜ VEFAT SAYISI','deaths_new'),\
('BUGÜNKÜ İYİLEŞEN SAYISI','rec_new')\
]

#prepare the dictionary for the data
data = {\
'date':'',\
'tests_total':'',\
'conf_total':'',\
'deaths_total':'',\
'severe_total':'',\
'intube_total':'',\
'rec_total':'',\
'tests_new':'',\
'conf_new':'',\
'deaths_new':'',\
'rec_new':'',\
}

#put the date
data['date'] = date

for item in items:
    #the data in placed inside two span tags, first->name, second->value
    spans = item.find_all('span')

    #extract the name, strip the new line chars (<br>), replace all excess whitespaces with single whitespace
    key = re.sub(' +', ' ',spans[0].text.replace('\n', ' ').replace('\r', '').strip())

    #now, map the turkish name into meta data
    for k, v in mapping2:
        key = key.replace(k, v)

    #extract the value, place the number without any digit formatting
    value = spans[1].text.strip().replace('.','')
    data[key] = value

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
sep='\t', end='\n')
