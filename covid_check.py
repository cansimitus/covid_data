import requests
import re
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
URL = 'https://covid19.saglik.gov.tr/'
page = requests.get(URL, verify=False)

soup = BeautifulSoup(page.content.decode('utf-8', 'ignore'), 'html.parser')
items = soup.find('div', {"class":"corona-bg"}).find_all('li', {"class": re.compile("d-flex justify-content-between baslik-k*")})
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

data['date'] = date

row=1
for item in items:
    spans = item.find_all('span')
    key = re.sub(' +', ' ', spans[0].text.replace('\n', ' ').replace('\r', '').strip())
    for k, v in mapping2:
        key = key.replace(k, v)
    value = spans[1].text.strip().replace('.','')
    data[key] = value
    row=row+1

print(data)
