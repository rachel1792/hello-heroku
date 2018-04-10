from datetime import date

import re
import requests
from bs4 import BeautifulSoup


def scrape():
    formatted_date = date.strftime(date.today(), '%m/%d/%Y')
    response = requests.get('https://www.xwordinfo.com/Crossword?date={}'.format(formatted_date))
    soup = BeautifulSoup(response.content, 'html.parser')


def parse(response):

    title = response.h1.text

    pattern = re.compile("New York Times")

    if pattern.match(title) is None:
        nyt, day, date, year = response.xpath('//h3[@id="CPHContent_SubTitleH3"]/text()').extract_first().split(',')
    else:
        nyt, day, date, year = title.split(',')
        title = ' '

    across = response.find_all(lambda tag: tag.has_attr('id') and tag['id'] == 'CPHContent_tdAcrossClues')[0]
    down = response.find_all(lambda tag: tag.has_attr('id') and tag['id'] == 'CPHContent_tdDownClues')[0]

    across_answers = [item.text for item in across.find_all('a')]
    down_answers = [item.text for item in down.find_all('a')]

    across_clues = re.split('[0-9]+\.| : ', across.text)[1::2]
    down_clues = re.split('[0-9]+\.| : ', down.text)[1::2]

    # debut_words = []
    # debut_words += across.xpath('.//span[@class="unique"]/text()').extract()
    # debut_words += down.xpath('.//span[@class="unique"]/text()').extract()
    #
    # debut_words += across.xpath('.//span[@class="debut"]/text()').extract()
    # debut_words += down.xpath('.//span[@class="debut"]/text()').extract()

    assert len(across_answers) == len(across_clues)
    assert len(down_answers) == len(down_clues)

    for i in range(len(across_answers)):
        answer = across_answers[i].encode('ascii', 'ignore').strip()
        clue = across_clues[i].encode('ascii', 'ignore').strip()

        clue = verify(clue)
        answer = verify(answer)
        title = verify(title)
        year = verify(year)
        day = verify(day)
        date = verify(date)

        item = CWItem()
        item['answer'] = answer
        item['clue'] = clue
        item['title'] = title

        item['year'] = year
        item['day'] = day
        item['date'] = date

        # if answer in debut_words:
        #     item['unique'] = 'True'
        # else:
        #     item['unique'] = 'False'

        yield item

    for i in range(len(down_answers)):
        answer = down_answers[i].encode('ascii', 'ignore').strip()
        clue = down_clues[i].encode('ascii', 'ignore').strip()

        clue = verify(clue)
        answer = verify(answer)
        title = verify(title)
        year = verify(year)
        day = verify(day)
        date = verify(date)

        item = CWItem()
        item['answer'] = answer
        item['clue'] = clue
        item['title'] = title

        item['year'] = year
        item['day'] = day
        item['date'] = date

        # if answer in debut_words:
        #     item['unique'] = 'True'
        # else:
        #     item['unique'] = 'False'
        #
        # yield item


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
