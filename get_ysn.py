import wget
import os
import zipfile

def main():
    file_name = 'data-20230425-structure-20180801.zip'
    if 'srn.zip' not in os.listdir('srn'):
        wget.download (f'https://data.nalog.ru/opendata/7707329152-snr/{file_name}', 'srn/srn.zip')
        while 'srn.zip' not in os.listdir('srn'):
            print('downloading')
        with zipfile.ZipFile('srn/srn.zip', 'r') as zip_ref:
            zip_ref.extractall('srn')
