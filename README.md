# covid_data
* My Work on Turkish COVID-19 Data
This repo is dedicated for my work on Turkish COVID-19 data, that is placed on the website https://covid19.saglik.gov.tr/.

** covid_check.py
This is the python web scrapper. It fetches the daily data and outputs in the format to be placed directly into covid_tr.txt

** covid.r
This is the basic R file for visualizing the data.

** covid_tr.txt
This is the actual data, tab-seperated text file, with the format:
date: d.mm.yyyy date of date
conf_new: confirmed cases for the current day
conf_total: confirmed cases total
deaths_new: deaths for the current day
deaths_total: deaths total
rec_new: recovered patients for the current day
rec_total: recovered patients total
intube_total: intubated patients for the current day
severe_total: severe patients for the current day, other than intubated
tests_new: tested patients for the current day
tests_total: tested patients total
