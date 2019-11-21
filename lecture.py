from bs4 import BeautifulSoup
import requests


def lecture():
    lecture_list = list()

    elem = requests.get(r'http://nclab.ssu.ac.kr/bbs/board.php?bo_table=course_sitemap')
    elem.encoding = None
    soup = BeautifulSoup(elem.text, 'html.parser')

    tables = soup.find_all('table', {'class': 'sitemap2'})

    for i in tables:
        _lecture = dict()

        lecture_name = i.find('strong').text.replace('_', '')
        _lecture['name'] = lecture_name.split(' ')[0]
        _lecture['semester'] = lecture_name.split(' ')[-1]

        temp = i.find_all('a')
        for j in temp:
            lecture_type = j.find('span').text
            _lecture[lecture_type] = './lecture/' + j.get('href').split('bo_table=')[1]

        lecture_list.append(_lecture)

    return lecture_list
