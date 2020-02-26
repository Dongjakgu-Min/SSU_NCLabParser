from bs4 import BeautifulSoup
import requests


def lecture():
    lecture_list = list()

    elem = requests.get(r'http://nclab.ssu.ac.kr/bbs/board.php?bo_table=course_sitemap')
    elem.encoding = None
    soup = BeautifulSoup(elem.text, 'html.parser')

    tables = soup.find_all('table', {'class': 'sitemap2'})

    for i in tables:
        lec = dict()

        lecture_name = i.find('strong').text.replace('_', '')
        lec['name'] = lecture_name.split('(')[0]
        lec['semester'] = lecture_name.split('(')[-1][:-1]

        temp = i.find_all('a')
        for j in temp:
            lecture_type = j.find('span').text
            lec[lecture_type] = j.get('href')

        lecture_list.append(lec)

    return lecture_list
