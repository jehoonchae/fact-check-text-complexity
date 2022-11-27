import csv
import json
import time
import argparse
from tqdm import tqdm

# from utils import get_soup
# from utils import str_date_to_datetime
# from utils import check_dir

from scraper.utils import get_soup
from scraper.utils import str_date_to_datetime
from scraper.utils import check_dir

base_url = 'https://www.politifact.com'
'https://www.politifact.com/factchecks/list/?page=650'
url = f'https://www.politifact.com/article/list/?page=1'
soup = get_soup(url)


url_list = []
for i in tqdm(range(650)):
    url = f'https://www.politifact.com/factchecks/list/?page={i+1}'
    soup = get_soup(url)
    if soup.find('div', class_='m-statement__quote'):
        article_list = soup.find_all('div', class_='m-statement__quote')
        for article in article_list:
            url_list.append(base_url + article.a.get('href'))

# with open('politifact_url.txt', 'w', encoding='utf-8') as f:
#     for url in url_list:
#         f.write(url + '\n')

with open('politifact_url.txt', 'r') as f:
    url_list = [url.replace('\n', '') for url in f.readlines()]

soup = get_soup('https://www.politifact.com/factchecks/2020/sep/16/tweets/twitter-video-does-not-show-drone-starting-west-co/')

article_dict = dict()
check_dir('./data/politifact.json')
with open('./data/politifact.json', 'w') as json_file:
    for i, url in enumerate(tqdm(url_list[1328:])):
        soup = get_soup(url)
        title = soup.find('div', class_='m-statement__quote').text.replace('\n', '')
        try:
            date = str_date_to_datetime(soup.find('span', class_='m-author__date').text)
        except:
            date = ''
        category = [list.find('span').text for list in soup.find_all('li', class_='m-list__item')]
        author_list = [author.div.a.text for author in soup.find_all('div', class_='m-author')]
        content = [p.text for p in soup.find('article', class_='m-textblock').find_all('p')]
        content = ' '.join(content)
        article_dict.update(
            {i: {'url': url, 'date': date, 'category': category, 'author': author_list, 'title': title, 'content': content}}
        )
    json.dump(article_dict, json_file)

soup = get_soup('https://www.politifact.com/factchecks/2021/mar/05/chris-kapanga/yes-marijuana-can-increase-risk-schizophrenia-and-/')
soup.find('div', class_='c-image')

soup.find('div', class_='m-statement__quote').text.replace('\n', '')

soup.find_all('div', class_='m-author')[0].div.a.text
