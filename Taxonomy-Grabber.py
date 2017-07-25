from bs4 import BeautifulSoup
from selenium import webdriver
from collections import deque
import re
import csv

page = "https://www.amazon.co.uk/Camping-Hiking-Tents-Sleeping-Bags/b/ref=nav_shopall_cphk?ie=UTF8&node=319545011"
hostname = "https://www.amazon.co.uk"
driver = webdriver.Chrome(executable_path='chromedriver')

category_tiles = 'acs-tiles-wrap'
category_sidebar = 'a-unordered-list a-nostyle a-vertical s-ref-indent-two'

queue = deque(["https://www.amazon.co.uk/Camping-Hiking-Tents-Sleeping-Bags/b/ref=nav_shopall_cphk?ie=UTF8&node=319545011"])
crawled = set()
tax =[]
bread =[]

class grab_links(object):

    def __init__(self):
        pass

    def breadcrumb(self,page,soup):
        results = soup.find('ul', attrs={'class': 'a-unordered-list a-nostyle a-vertical a-spacing-base'})
        core = []
        cleaned = []
        try:
            cats = results.findAll('li',attrs={'class':'s-ref-indent-neg-micro'})
            for i in cats:
                core.append(i.text)
            cats2 = results.findAll('li',attrs={'class':'s-ref-indent-one'})
            for i in cats2:
                core.append(i.text)
            for value in core:
                i = re.sub('  ','',value)
                i = re.sub('\n', '', i)
                cleaned.append(i)
            row = ','.join(cleaned)
            bread.append((page,row))
        except:
            pass

    def category_grab(self,page,soup):
        results = soup.findAll('div', attrs={'class': category_tiles})
        title = soup.title.text
        links = []
        for a in results:
            link = a.findAll('a')
            [links.append(i) for i in link]
        for i in links:
            if i['href'].find(hostname) == -1:
                link = hostname+i['href']
                if link not in crawled:
                    queue.append(link)
                    crawled.add(link)
                    tax.append((page,link))
            elif i['href'] not in crawled:
                queue.append(i['href'])
                crawled.add(i['href'])
                tax.append((page, i['href']))


    def sidebar_grab(self,page,soup):
        results = soup.findAll('ul', attrs={'class': category_sidebar})
        title = soup.title.text
        links = []
        for a in results:
            link = a.findAll('a')
            [links.append(i) for i in link]
        for i in links:
            if i['href'].find(hostname) == -1:
                link = hostname + i['href']
                if link not in crawled:
                    queue.append(link)
                    crawled.add(link)
                    tax.append((page, link))
            elif i['href'] not in crawled:
                queue.append(i['href'])
                crawled.add(i['href'])
                tax.append((page, i['href']))


def save_tax():
    for mapping in tax:
        with open('taxonomy.csv',mode='a',encoding="utf-8") as file:
            file.write("{},{}\n".format(mapping[0],mapping[1]))

    with open('bread.csv',mode='a',encoding="utf-8") as file:
        for row in bread:
            file.write("{},{}\n".format(row[0], row[1]))


if __name__ == "__main__":
    while len(queue):
        print(len(queue))
        url = queue.popleft()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source)
        int = grab_links()
        int.category_grab(url, soup)
        int.sidebar_grab(url,soup)
        int.breadcrumb(url, soup)
    save_tax()
