import csv
import json
import time
import argparse
from tqdm import tqdm
import os.path
import pandas as pd

# from utils import get_soup
# from utils import str_date_to_datetime
# from utils import check_dir

from scraper.utils import get_soup
from scraper.utils import str_date_to_datetime
from scraper.utils import check_dir

def factcheckorg_url_scraper(csv_output_path=None):
    """
    :param csv_output_path: file path to save csv
    :return: url list of articles
    """
    url_list = []
    if csv_output_path == None:
        for i in tqdm(range(304), desc='Scraping URL of fact-checking news at FactCheckOrg'):
            base_url = f'https://www.factcheck.org/the-factcheck-wire/page/{str(i + 1)}'
            soup = get_soup(base_url)
            time.sleep(1)
            article_url_list = soup.find_all('article')
            for article in article_url_list:
                url = article.find('h3').a.get('href')
                url_list.append(url)
    else:
        check_dir(csv_output_path)
        with open(csv_output_path, 'w') as f:
            writer = csv.writer(f)
            header_row = ['url', 'date', 'org', 'title', 'summary']
            writer.writerow(header_row)
            for i in tqdm(range(304)):
                base_url = f'https://www.factcheck.org/the-factcheck-wire/page/{str(i + 1)}'
                soup = get_soup(base_url)
                article_url_list = soup.find_all('article')
                for article in article_url_list:
                    url = article.find('h3').a.get('href')
                    date = str_date_to_datetime(article.find('div', class_='entry-meta').text.strip())
                    org = 'factcheckorg'
                    title = article.find('h3').text
                    summary = article.find('div', class_='entry-content').text.strip()
                    article_info_list = [url, date, org, title, summary]
                    writer.writerow(article_info_list)
                    url_list.append(url)
    return url_list


def factcheckorg_article_scraper(json_output_path, csv_output_path=None):
    """

    :param json_output_path:
    :param csv_output_path:
    :return:
    """
    if os.path.isfile('factcheckorg_url.csv'):
        df = pd.read_csv('factcheckorg_url.csv')
        url_list = df['url'].tolist()
    else:
        url_list = factcheckorg_url_scraper(csv_output_path)
    factcheck_dict = dict()
    if type(json_output_path) != str:
        json_output_path = str(json_output_path)
    check_dir(json_output_path)
    with open(json_output_path, 'w') as json_file:
        for i, url in enumerate(tqdm(url_list, desc='Scraping fact-checking news articles')):
            soup = get_soup(url)
            date = str_date_to_datetime(soup.find('p', class_='posted-on').time.text)
            try:
                category = [li.text.replace('\n', '') for li in soup.find('li', class_='categories').find_all('li')]
            except:
                category = []
            try:
                tags = [li.text.replace('\n', '') for li in soup.find('li', class_='post_tag').find_all('li')]
            except:
                tags = []
            try:
                location = [li.text.replace('\n', '') for li in soup.find('li', class_='location').find_all('li')]
            except:
                location = []
            try:
                issue = [li.text.replace('\n', '') for li in soup.find('li', class_='issue').find_all('li')]
            except:
                issue = []
            try:
                people = [li.text.replace('\n', '') for li in soup.find('li', class_='person').find_all('li')]
            except:
                people = []
            title = soup.find('header', class_='entry-header').h1.text
            author_list = [author.text for author in soup.find('div', class_='entry-meta').find_all('a')]
            content = [p.text for p in soup.find('div', class_='entry-content').find_all('p')]
            content = ' '.join(content)
            factcheck_dict.update(
                {i: {'url': url, 'date': date, 'author': author_list,
                     'category': category, 'tags': tags, 'location': location, 'people': people,
                     'issue': issue, 'title': title, 'content': content}})
        json.dump(factcheck_dict, json_file)

factcheckorg_article_scraper(json_output_path='./data/factcheckorg.json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Argument for output paths')
    parser.add_argument('article_json_output', type=str, help='Path of scraped article. JSON type should be given.')
    parser.add_argument('--url_csv_output', type=str, default=None, help='Path of URL output')
    args = parser.parse_args()
    factcheckorg_article_scraper(args.article_json_output, args.url_csv_output)
