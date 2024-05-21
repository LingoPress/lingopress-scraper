from xml.etree import ElementTree
import requests

from escape_xml_illegal_chars import escape_xml_illegal_chars


class RssScraper:
    def __init__(self, rss_url):
        self.rss_url = rss_url
        rss = requests.get(self.rss_url)
        rss.encoding = 'utf-8'  # Ensure the response is interpreted as UTF-8
        rss_content = rss.text.encode('utf-8', errors='ignore').decode('utf-8')  # Handle any encoding issues
        result_chars = escape_xml_illegal_chars(rss_content)
        self.root = ElementTree.fromstring(result_chars)
        self.rss = rss_content

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
