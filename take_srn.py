import xml.etree.ElementTree as ET
import os

def main(inn):
    files_list = os.listdir('srn')
    for fl in files_list:
        res = parse_snr(fl, inn)
            if res:
                return res

def parse_snr(string, inn):
    root = ET.fromstring(string)
    range_fin = len(root)
    fn = lambda x: root[x][0].attrib['ИННЮЛ']
    for it in range(1, range_fin):
        if inn == fn(it):
            dic = root[it][1].attrib
            for key, value in dic.items():
                if value == '1':
                    print('Данные об СРН найдены в базе данных ФНС')
                    return key[5:]
    return