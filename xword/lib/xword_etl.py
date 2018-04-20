from datetime import date

import re
import requests
from bs4 import BeautifulSoup


def extract():
    formatted_date = date.strftime(date.today(), '%m/%d/%Y')
    response = requests.get('https://www.xwordinfo.com/Crossword?date={}'.format(formatted_date))
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def transform(response):

    title = response.h1.text

    pattern = re.compile("New York Times")

    if pattern.match(title) is None:
        nyt, day, date, year = response.xpath(
            '//h3[@id="CPHContent_SubTitleH3"]/text()').extract_first().split(',')
    else:
        nyt, day, date, year = title.split(',')
        title = ' '

    across = response.find_all(
        lambda tag: tag.has_attr('id') and tag['id'] == 'CPHContent_tdAcrossClues')[0]
    down = response.find_all(
        lambda tag: tag.has_attr('id') and tag['id'] == 'CPHContent_tdDownClues')[0]

    across_answers = [item.text for item in across.find_all('a')]
    down_answers = [item.text for item in down.find_all('a')]

    across_clues = re.split('[0-9]+\.| : ', across.text)[1::2]
    down_clues = re.split('[0-9]+\.| : ', down.text)[1::2]

    unique_words = response.find_all('span', 'unique')

    debut_words = response.find_all('span', 'debut')

    return dict(
        title=title,
        across_answers=across_answers,
        across_clues=across_clues,
        down_answers=down_answers,
        down_clues=down_clues,
    )


def load(content):
    pass


def verify(content):
    if isinstance(content, list):
        if len(content) > 0:
            content = content[0]
            # convert unicode to str
            return content.encode('ascii', 'ignore')
        else:
            return ""
    else:
        # convert unicode to str
        return content.encode('ascii', 'ignore')
