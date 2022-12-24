from bs4 import BeautifulSoup
import requests
import datetime as dt
from collections import Counter

r = requests.get('https://panorama.pub/')
page = r.content.decode("utf-8")
soup = BeautifulSoup(page, 'html.parser')


async def get_agg_news(start, end):
    ans = []
    format = '%d-%m-%Y'

    curr_date = dt.datetime.strptime(start, format)
    end_date = dt.datetime.strptime(end, format) + dt.timedelta(days=1)
    while curr_date != end_date:
        str_date = dt.datetime.strftime(curr_date, format)
        try:
            page = BeautifulSoup(requests.get('https://panorama.pub/news/' + str_date).content.decode("utf-8"),
                                 'html.parser')
            for x in page.find_all('div', attrs={'class': "grid"})[0].find_all('a'):
                rating = x.find_all('div')[2].get_text().strip()
                comments = x.find_all('div')[3].get_text().strip()
                ref = 'https://panorama.pub' + x.get('href')
                name = x.find_all('div')[4].get_text().strip()
                ans.append((name, ref, rating, comments))
        except:
            curr_date += dt.timedelta(days=1)
            continue
        curr_date += dt.timedelta(days=1)
    return ans


async def get_sections(s, start, end):
    d = {'Политика': 'politics', 'Общество': 'society', 'Наука': 'science', 'Экономика': 'economics'}
    section = d[s]
    ans = []
    format = '%d-%m-%Y'

    curr_date = dt.datetime.strptime(start, format)
    end_date = dt.datetime.strptime(end, format) + dt.timedelta(days=1)
    while curr_date != end_date:
        str_date = dt.datetime.strftime(curr_date, format)
        try:
            page = BeautifulSoup(
                requests.get('https://panorama.pub/' + section + '/' + str_date).content.decode("utf-8"),
                'html.parser')
            for x in page.find_all('div', attrs={'class': "grid"})[0].find_all('a'):
                rating = x.find_all('div')[2].get_text().strip()
                comments = x.find_all('div')[3].get_text().strip()
                ref = 'https://panorama.pub' + x.get('href')
                name = x.find_all('div')[4].get_text().strip()
                ans.append((name, ref, rating, comments))
        except:
            curr_date += dt.timedelta(days=1)
            continue
        curr_date += dt.timedelta(days=1)
    return ans


async def get_top_commentators(s, end):
    format = '%d-%m-%Y'

    end_date = dt.datetime.strptime(end, format) + dt.timedelta(days=1)
    section = 'news'
    comments = []
    curr_date = dt.datetime.strptime(s, format)
    while curr_date != end_date:
        str_date = dt.datetime.strftime(curr_date, format)

        try:
            page = BeautifulSoup(
                requests.get('https://panorama.pub/' + section + '/' + str_date).content.decode("utf-8"),
                'html.parser')
            if page.find('h1').get_text().strip() != 'Страница не найдена':
                for x in page.find_all('div', attrs={'class': 'grid'})[0].find_all('a'):
                    ref = 'https://panorama.pub' + x.get('href')
                    news_page = BeautifulSoup(requests.get(ref).content.decode("utf-8"), 'html.parser')
                    if news_page.find('h1').get_text().strip() != 'Страница не найдена':
                        for autor in news_page.find('div',
                                                    attrs={'itemtype': 'http://schema.org/NewsArticle'}).find_all(
                            'strong', attrs={'itemprop': 'author'}):
                            autor_name = autor.get_text().strip()
                            if len(autor_name) > 2:
                                comments += [autor_name]
        except:
            curr_date += dt.timedelta(days=1)
            continue
        curr_date += dt.timedelta(days=1)
    ans = ''
    for i, c in enumerate(Counter(comments).most_common(5)):
        ans += '{} - {} | Количество комментариев: {} \n'.format(i + 1, c[0], c[1])
    return ans
