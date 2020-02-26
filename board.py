from bs4 import BeautifulSoup
import requests


class Board:
    def __init__(self, url):
        elem = requests.get(url)
        elem.encoding = None

        self.documents = list()
        self.url = url
        self.soup = BeautifulSoup(elem.text, 'html.parser')

    def _get_documents(self, soup):
        for i in soup.select('tbody > tr'):
            document = dict()

            if i.find('td', {'class': 'empty_table'}):
                break

            document['title'] = i.find('td', {'class': 'td_subject'}).text.strip()
            document['link'] = i.find('a').get('href')
            document['date'] = i.find('td', {'class': 'td_date'}).text.strip()
            document['access'] = i.find('td', {'class': 'td_num'}).text.strip()

            if i.find('span', {'class': 'sv_member'}):
                document['owner'] = i.find('span', {'class': 'sv_member'}).text
            else:
                document['owner'] = i.find('span', {'class': 'sv_guest'}).text

            self.documents.append(document)

    def get_document(self):
        page = self.soup.select('a[class=pg_page]')
        url_list = [self.url]

        for i, p in enumerate(page):
            if p.text is None:
                continue
            url_list.append(self.url + '&page={0}'.format(i+2))

        print(url_list)

        for url in url_list:
            elem = requests.get(url)
            elem.encoding = None

            soup = BeautifulSoup(elem.text, 'html.parser')
            self._get_documents(soup)

        return self.documents
