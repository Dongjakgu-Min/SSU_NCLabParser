from bs4 import BeautifulSoup
import requests

from .document import Document


class Board:
    def __init__(self, url):
        elem = requests.get(r'http://nclab.ssu.ac.kr/bbs2/board.php?bo_table=' + url)
        elem.encoding = None

        self.documents = list()
        self.url = r'http://nclab.ssu.ac.kr/bbs2/board.php?bo_table=' + url
        self.soup = BeautifulSoup(elem.text, 'html.parser')

    def _get_documents(self):
        for i in self.soup.select('tbody > tr'):
            document = dict()

            document['title'] = i.find('td', {'class': 'td_subject'}).text.strip()
            document['link'] = i.find('a').get('href')
            document['owner'] = i.find('span', {'class': 'sv_member'}).text
            document['date'] = i.find('td', {'class': 'td_date'}).text.strip()
            document['access'] = i.find('td', {'class': 'td_num'}).text.strip()

            _attachment = Document(document['link'])
            document['attach'] = _attachment.get_attach()

            self.documents.append(document)

    def get_document(self):
        page = self.soup.select('a[class=pg_page]')
        url_list = [self.url]

        if self.soup.find_all('td', {'class': 'empty_table'}):
            return self.documents

        for i, p in enumerate(page):
            if p.text is None:
                continue
            url_list.append(self.url + '&page={0}'.format(i+2))

        for url in url_list:
            elem = requests.get(url)
            elem.encoding = None

            self._get_documents()

        return self.documents
