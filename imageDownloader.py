import requests
from bs4 import BeautifulSoup


def getUrl(word):
    html = requests.get('https://www.google.com/search?q=' +
                        word + '&tbm=isch').text
    soup = BeautifulSoup(html, 'html.parser')

    return soup.find_all('img')[1]['src']


if __name__ == '__main__':
    print(getUrl('Plant'))

    # for img in soup.find_all('img'):
    #    print(img['src'])
