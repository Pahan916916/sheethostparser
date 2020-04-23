import os, re, json, requests, random, time, argparse
import urllib.parse as urlparse
from urllib.parse import parse_qs
from bs4 import BeautifulSoup

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Sheet:
    __title: str
    __true_url: str

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def true_url(self):
        return self.__true_url

    @true_url.setter
    def true_url(self, true_url):
        self.__true_url = true_url

def query_validation(query1, query2):
    if len(list(set(list(query1.lower().split())) & set(list(query2.lower().split())))) != 0:
        return True
    else:
        return False

def getSheetHostLinks(url, query):
    list_PlaylistLinks = []

    sourceCode = requests.get(url).text
    soup = BeautifulSoup(sourceCode, 'html.parser')

    for link in soup.find_all('tr'):
        sheet = Sheet()
        
        if query.lower() in str(link).lower():

            sourceCode = str(link)
            soup = BeautifulSoup(sourceCode, 'html.parser')

            little_soup = soup.find('a', class_='score-title')

            sheet.title = str(little_soup.getText()).strip()
            sheet.true_url = str(little_soup.get('href')).strip()

            list_PlaylistLinks.append(sheet)
    
    download_link_finder(list_PlaylistLinks)   

    
def download_link_finder(links_array):
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Cookie': 'autologin=a%3A2%3A%7Bs%3A7%3A%22user_id%22%3Bs%3A4%3A%225159%22%3Bs%3A3%3A%22key%22%3Bs%3A16%3A%222a4cdf5b28b85d12%22%3B%7D; 0ci_session=P7YIeN%2BYf4rZ%2F19XFB%2FxeK2wh0k0GbTqRmw0FcechiNWNreWdG%2FNgOSdTrHu0pjHxiKS7lSezfFxtgJfVAswdWW5O%2F1AM5z5QOQi1izxgq%2BY0pXuVFUPtILucGbukPjA13H2DO3gOYK0B7s3PhKs4I4eRP624VPmhyZVrMzna%2FH5s5GWbo4C1I3zTa3jQZVjbEMCEROiDTTw7X%2F4AagPJMnGUgxqgyNbdNGgDtYIEzZE0DOpucQRHAtnRsjdc3a%2FuiJAR4zHxj4TJstkGXrFjGOQrYhjvZlwBIPD3E%2FzdWWADTIR8%2BIcDxxenlH1zSMn2hxqVa1dR3qlNWhdBrxYX0xNOj0dR4dvYkO%2FTUvuDt9B5P9i6uk9WFo3hncfgZbUzYSnqLLkKuX7SkgUk%2FL0Nld6MI9rUWT2x3jv6mZcMsw%3D'}
    
    for i in links_array:
        sourceCode = requests.get(i.true_url,headers=headers).text
        soup = BeautifulSoup(sourceCode, 'html.parser')

        little_soup = soup.find('div', class_='well sheet-download')

        sourceCode = str(little_soup)
        soulittle_soup = BeautifulSoup(sourceCode, 'html.parser')

        for li in soulittle_soup.find_all('li'):
            sourceCode = str(li)
            soulittle_soup = BeautifulSoup(sourceCode, 'html.parser')

            soup = soulittle_soup.find('a')
            
            if '.pdf' in soup.getText():
                sheets_downloader(i.title, soup.get('href'))
                print(f'{i.title}.pdf Сохранено')


def sheets_downloader(save_filename, link):
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Cookie': 'autologin=a%3A2%3A%7Bs%3A7%3A%22user_id%22%3Bs%3A4%3A%225159%22%3Bs%3A3%3A%22key%22%3Bs%3A16%3A%222a4cdf5b28b85d12%22%3B%7D; 0ci_session=P7YIeN%2BYf4rZ%2F19XFB%2FxeK2wh0k0GbTqRmw0FcechiNWNreWdG%2FNgOSdTrHu0pjHxiKS7lSezfFxtgJfVAswdWW5O%2F1AM5z5QOQi1izxgq%2BY0pXuVFUPtILucGbukPjA13H2DO3gOYK0B7s3PhKs4I4eRP624VPmhyZVrMzna%2FH5s5GWbo4C1I3zTa3jQZVjbEMCEROiDTTw7X%2F4AagPJMnGUgxqgyNbdNGgDtYIEzZE0DOpucQRHAtnRsjdc3a%2FuiJAR4zHxj4TJstkGXrFjGOQrYhjvZlwBIPD3E%2FzdWWADTIR8%2BIcDxxenlH1zSMn2hxqVa1dR3qlNWhdBrxYX0xNOj0dR4dvYkO%2FTUvuDt9B5P9i6uk9WFo3hncfgZbUzYSnqLLkKuX7SkgUk%2FL0Nld6MI9rUWT2x3jv6mZcMsw%3D'}

    save_filename = save_filename.replace('/', '').replace('\\', '').replace(':', '').replace('|', '').replace('*', '').replace('"', '').replace('<', '').replace('>', '').replace('?', '')

    file_save = os.path.join(BASE_DIR, f'{save_filename}.pdf')

    if os.path.exists(file_save):
        pass
    else:
        obj=requests.get(link ,headers=headers)
        with open(file_save, mode='wb') as file:
            file.write(obj.content)

def finder(query):
    category_list = ['video-game', 'anime','movie','tv','classical','pop','jazz-and-blues','contemporary','rock','other']

    for i in category_list:
        getSheetHostLinks(f'https://sheet.host/category/{i}', query)
    print('Закончил')



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='query\n')

	parser.add_argument('query', type=str, nargs='*',
	                        help='query')

	args = parser.parse_args()
	vargs = vars(args)


	if not vargs['query']:
	    parser.error('Query is not found')
	else:
		finder(' '.join(vargs['query']))

		