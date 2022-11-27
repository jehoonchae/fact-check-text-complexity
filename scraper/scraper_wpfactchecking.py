from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import random
import time
from datetime import datetime


# options = webdriver.ChromeOptions()
# options.add_argument("headless")
# options.add_argument("window-size=1920x1080")
# options.add_argument("disable-gpu")
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)  # With headless mode

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.implicitly_wait(10)

base_url = 'https://www.washingtonpost.com/news/fact-checker/wp/2021/02/?arc404=true'
base_url = 'https://www.nytimes.com/search?dropmab=false&endDate=20210228&query=&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=best&startDate=20181231&types=article'

driver.get(base_url)
sleep_time = random.random() * 3
time.sleep(sleep_time)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

element = driver.find_element_by_xpath('//*[@id="site-content"]/div/div[2]/div[2]/div/button')
element.click()
for _ in range(100):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    element.click()
    time.sleep(1.5)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

len(soup.find_all('li', class_='css-1l4w6pd'))
import csv
with open('nyt_url_3.csv', 'w') as f:
    writer = csv.writer(f)
    header_row = ['url', 'date', 'category', 'press', 'title']
    writer.writerow(header_row)
    for li in soup.find_all('li', class_='css-1l4w6pd'):
        date = li.find('span', class_='css-17ubb9w').text
        # if 'Dec' not in date:
        #     date = datetime.strptime(date, '%b. %d').strftime('%m-%d')
        #     date = '2021-' + date
        # else:
        #     date = datetime.strptime(date, '%b. %d, %Y').strftime('%Y-%m-%d')
        date = datetime.strptime(date, '%b. %d, %Y').strftime('%Y-%m-%d')
        url = li.find('div', class_='css-e1lvw9').a.get('href')
        url = 'https://www.nytimes.com' + url
        category = li.find('p', class_='css-myxawk').text
        title = li.find('h4', class_='css-2fgx4k').text
        article_info_list = [url, date, category, 'nyt', title]
        writer.writerow(article_info_list)

soup.find('div', class_=re.compile('loadmore')).text
before_len = len(soup.find_all('div', class_='story-headline'))
element = driver.find_element_by_xpath('//*[@id="fUmJ2x1JaFtCds"]/div/div[1]/div[2]')
element.click()
after_len = len(soup.find_all('div', class_='story-headline'))

soup.find_all('div', class_='story-headline')[1].find_all('div')

url_list = []
base_url = 'https://www.washingtonpost.com'
for p in tqdm(soup.find_all('div', class_='story-list-story row item')):
    url_list.append(base_url + p.find('h2').a.get('href'))

soup.find_all('div', class_='story-list-story row item')[1].find('h2').a.get('href')

with open('wpfactchecking_url.txt', 'w', encoding='utf-8') as f:
    for url in url_list:
        f.write(url + '\n')


myLength = len(WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='story-headline']"))))
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pb-loadmore-div-ans button pb-loadmore clear']"))).click()
        WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_xpath("//div[@class='story-headline']")) > myLength)
        # titles = driver.find_elements_by_xpath("//div[@class='title']")
        # urls = driver.find_element_by_css_selector('')
        # html = driver.page_source
        # soup = BeautifulSoup(html, 'lxml')
        # titles = soup.find_all('div', class_='story-headline')
        # urls = [article.h2.get('href') for article in soup.find_all('div', class_='story-headline')]
        titles = driver.find_elements_by_xpath("//div[@class='story-headline']")
        myLength = len(titles)
    except TimeoutException:
        break
print(len(a))
titles[0]
len(titles)
title_list = [title.text for title in titles]
for title in titles:
    print(title.find_element_by_xpath("//div[@class='story-headline']/h2/a").get_attribute('href'))
url_list = [title.find_element_by_xpath("//div[@class='story-headline']/h2/a").get_attribute('href') for title in titles]
url_list