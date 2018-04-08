from datetime import date

import requests
from bs4 import BeautifulSoup


formatted_date = date.strftime(date.today(), '%m/%d/%Y')
response = requests.get('https://www.xwordinfo.com/Crossword?date={}'.format(formatted_date))
soup = BeautifulSoup(response.content, 'html.parser')
