from bs4 import BeautifulSoup
import requests


class Document:
    def __init__(self, url):
        elem = requests.get(url)
        elem.encoding = None

        self.soup = BeautifulSoup(elem.text, 'html.parser')
        self.attach = list()
        self.comment = list()
        self.content = dict()

    def get_attach(self):
        attachment = self.soup.select('section[id=bo_v_file] > ul > li')

        for obj in attachment:
            attachment_elem = dict()
            name, size = obj.find('a').text.replace(' ', '').strip().split('\n')

            attachment_elem['file'] = name.strip()
            attachment_elem['file_size'] = size.strip()
            attachment_elem['file_link'] = obj.find('a').get('href')
            attachment_elem['date'] = obj.find('span', {'class': None}).text

            self.attach.append(attachment_elem)

        return self.attach

    def get_comment(self):
        comment = self.soup.find('section', {'id': 'bo_vc'})

        for obj in comment.find_all('article'):
            comment_elem = dict()

            comment_elem['member'] = obj.find('span', {'class': 'member'}).text
            comment_elem['date'] = obj.find('time').text
            comment_elem['content'] = obj.find('p').text

            self.comment.append(comment_elem)

        return self.comment

    def get_content(self):
        info = self.soup.find('section', {'id': 'bo_v_info'})

        self.content['content'] = self.soup.find('div', {'id': 'bo_v_con'}).text
        self.content['member'] = info.find('span', {'class': 'sv_member'}).text
        self.content['date'] = info.find_all('strong')[1].text

        return self.content
