import logging
import table_search
import requests
import wget
import fitz
import os
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def main(inn):
    search_item = inn
    try:
        link = get_link()
    except requests.exeptions.ConnectionError as e:
        print(e)
        table_search.main(inn)
    if not link:
        if read_pdf(search_item):
            return 'Актуальный список иноагентов в настоящий момент не доступен\nПо данным последнего доступного реестра объект ЯВЛЯЕТСЯ иноагентом\n'
        else:    
            return 'Актуальный список иноагентов в настоящий момент не доступен\nПо данным последнего доступного реестра объект НЕ является иноагентом\n'
    else:
        print(f'Link is found ===> {link}')
        lnk = get_pdf(link)
    if read_pdf(search_item):
        return 'Объект является иноагентом'
    else:
        return 'Объект НЕ является иноагентом'

def get_link():
    print('getting the link')
    url = 'https://minjust.gov.ru/ru/activity/directions/942/'
    html_doc = requests.get(url, headers=headers)
    print(html_doc)
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
    if doc.status == 200:
        open('doc.pdf', 'wb').write(doc.content)
    else:
        print(doc.status)

def read_pdf(search_item):
    doc = fitz.open('doc.pdf')
    page_count = doc.page_count
    print(f'Number of pages {page_count}')
    for i in range(page_count):
        text = doc[i-1].get_text()
        if search_item in text:
            return True

if __name__ == '__main__':
    main(7725275206)


