import fitz
import sqlite3
import os
import inoagent_search
import re

class Person:
    def __init__(self, block):
        self.block = block
        self.find_name()
        self.find_bdate()
        self.find_inn()

    def find_name(self):
        res = re.search('(\d{1,4})\s(\w+\D)\s(\w+\D)\s(\w+\D)\s', self.block)
        if res:
            self.number = res.group(1)
            self.first_name = res.group(2)
            self.second_name = res.group(3)
            self.paternal = res.group(4)

    def find_bdate(self):
        res = re.search('\d{2}\.\d{2}\.\d{4}', self.block)
        if res:
            self.birth_date = res.group(0)

    def find_inn(self):
        res = re.search('\d{12}', self.block)
        if res:
            self.inn = res.group(0)
        else:
            self.inn = ''

def check_db():
    if not 'inoagents.db' in os.listdir('/home/git/databases'):
        con = sqlite3.connect('/home/git/databases/inoagents.db')
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS inoagents (number, inn, organization, first_name, second_name, paternal, birthdate)")
        print('table created')
        con.commit()
        con.close()

def fill_base():
    doc = fitz.open('inoagents.pdf')
    page_count = doc.page_count
    numbers_list = []
    text_join = []
    text_blocks_fl = []
    text_blocks_ul = []

    for i in range(page_count):
        text = doc[i-1].get_text()
        text_join.append(text)
    joined_text = ''.join(text_join)

    numbers = re.findall('\n\d{1,4}\n',joined_text)

    for it in numbers:
        numbers_list.append(joined_text.index(it))

    slices = [(it1, it2) for it1, it2 in zip(numbers_list[::2], numbers_list[1::2])]
    
    for itm in slices:
        blck = joined_text[itm[0]:itm[1]]
        if re.search('\d{1,4}\s(\w+\D)\s(\w+\D)\s(\w+\D\S)\s\d{2}\.\d{2}\.', blck):
            text_blocks_fl.append(blck)
        else:
            print(blck)
            input()
            text_blocks_ul.append(blck)
    return text_blocks_fl, text_blocks_ul

def put_to_table(per):
    con = sqlite3.connect('/home/git/databases/inoagents.db')
    cur = con.cursor()
    cur.execute("INSERT INTO inoagents VALUES (?,?,?,?,?,?,?)", [per.number, per.inn, '', per.first_name, per.second_name, per.paternal, per.birth_date])
    con.commit()
    con.close()


def main():
    check_db()
    res = fill_base()
    for item in res[0]:
        per = Person(item)
        put_to_table(per)

if __name__ == '__main__':
    main()

