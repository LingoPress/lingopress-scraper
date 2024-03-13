from xml.etree import ElementTree
import requests


class RssScraper:
    def __init__(self, rss_url):
        self.rss_url = rss_url
        rss = requests.get(self.rss_url)
        self.root = ElementTree.fromstring(rss.content)
        # self.rss = rss.text
        self.rss = rss

    def get_rss(self):
        return self.rss

    def get_press_urls(self, limit=5):
        # 나중엔 robots.txt 를 확인해서 문제있는 엔드포인트 들은 삭제하도록.
        urls = []
        for item in self.root.iter('item'):
            url = item.find('link').text
            urls.append(url)
        urls = urls[:limit]
        return urls
