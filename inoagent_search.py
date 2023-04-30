import logging
import requests
import wget
import fitz
import os
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def main(inn):
    search_item = inn
    link = get_link()
    lnk = get_pdf(link)
    if not lnk:
        return 'Список иноагентов в настоящий момент не доступен'
    if read_pdf(search_item):
        return 'Объект является иноагентом'
    else:
        return 'Объект НЕ является иноагентом'

def get_link():
    url = 'https://minjust.gov.ru/ru/activity/directions/942/'
    html_doc = requests.get(url, headers=headers)
    if html_doc:
        print(f'site loaded...\n{html_doc.status_code}\n\n\n')
    else:
        print(f'some problems with site...\n{html_doc.status_code}\n\n\n')
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    res = soup.find_all('a')
    for item in res:
        link = item.get('href')
        if 'reestr-inostrannyih-agentov' in link:
            return link
        else:
            return False


def get_pdf(link):
    doc = requests.get(f'https://minjust.gov.ru{link}', headers=headers)
    open('doc.pdf', 'wb').write(doc.content)

def read_pdf(search_item):
    doc = fitz.open('doc.pdf')
    page_count = doc.page_count
    print(f'Number of pages {page_count}')
    for i in range(page_count):
        text = doc[i-1].get_text()
        if search_item in text:
            return True

if __name__ == '__main__':
    main()


