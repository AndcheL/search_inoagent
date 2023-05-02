import xml.etree.ElementTree as ET
import os

def main(inn):
    files_list = os.listdir('srn')
    for fl in files_list:
        if fl.endswith('.xml'):
            res = parse_snr(f'srn/{fl}', inn)
            if res == 2:
                return 'Данные об СРН найдены в базе данных ФНС'
    return 'Данные об СРН НЕ найдены в базе данных ФНС'

def parse_snr(fl, inn):
    tree = ET.parse(fl)
    root = tree.getroot()
    range_fin = len(root)
    fn = lambda x: root[x][0].attrib['ИННЮЛ']
    for it in range(1, range_fin):
        res_inn = fn(it)
        if inn == res_inn:
            dic = root[it][1].attrib
            for key, value in dic.items():
                if value == '1':
                    return 2
