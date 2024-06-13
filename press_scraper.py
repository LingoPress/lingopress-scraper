from dateutil.parser import parse
from newspaper import Article
from newspaper import Config


class PressScraper:


    def __init__(self, url, language):
        self.url = url

        # config
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
        config = Config()
        config.browser_user_agent = user_agent
        config.request_timeout = 10

        language = language.lower()
        # en lang setting
        if language == 'en-us':
            language = 'en'
        self.article = Article(url, language=language, config=config)
        self.article.download()
        self.article.parse()

    def get_title(self):
        return self.article.title

    def get_text(self):
        # return self.article.text.split('\n')
        return self.article.text

    def get_url(self):
        return self.article.url

    def get_source_url(self):
        return self.article.source_url

    def get_publish_date(self):
        PUBLISH_DATE_TAGS = [
            {'attribute': 'property', 'value': 'rnews:datePublished',
             'content': 'content'},
            {'attribute': 'property', 'value': 'article:published_time',
             'content': 'content'},
            {'attribute': 'name', 'value': 'OriginalPublicationDate',
             'content': 'content'},
            {'attribute': 'itemprop', 'value': 'datePublished',
             'content': 'datetime'},
            {'attribute': 'property', 'value': 'og:published_time',
             'content': 'content'},
            {'attribute': 'name', 'value': 'article_date_original',
             'content': 'content'},
            {'attribute': 'name', 'value': 'publication_date',
             'content': 'content'},
            {'attribute': 'name', 'value': 'sailthru.date',
             'content': 'content'},
            {'attribute': 'name', 'value': 'PublishDate',
             'content': 'content'},
            {'attribute': 'pubdate', 'value': 'pubdate',
             'content': 'datetime'},
        ]
        for known_meta_tag in PUBLISH_DATE_TAGS:
            meta_tags = self.article.extractor.parser.getElementsByTag(
                self.article.clean_doc,
                attr=known_meta_tag['attribute'],
                value=known_meta_tag['value'])
            if meta_tags:
                date_str = self.article.extractor.parser.getAttribute(
                    meta_tags[0],
                    known_meta_tag['content'])
                datetime_obj = parse(date_str)
                if datetime_obj:
                    return datetime_obj

        return None
        # return self.article.publish_date

    def get_top_image(self):
        return self.article.top_image

    def get_authors(self):
        return self.article.authors

    def get_publisher(self):
        if self.article.source_url.__contains__("globalvoices.org"):
            return "Global Voices"
