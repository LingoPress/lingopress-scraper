from datetime import datetime
from press_scraper import PressScraper
from rss_scraper import RssScraper
from press_db_service import *


def rss_based_news_scraper(language, rss, nlp_model):
    # 1. rss 에 있는 기사 리스트 크롤링
    rss_scraper = RssScraper(rss)
    # 크롤링할 뉴스 수, 기본값은 5개
    news_urls = rss_scraper.get_press_urls(3)
    #
    # 2. 기사별로 스크래핑

    news_list = []
    for need_url in news_urls:
        crawler = PressScraper(need_url, language)
        # news_list에 기사 정보를 저장

        # 기사 제목에 " · Global Voices 日本語"가 포함되어있는 경우 제거
        title = crawler.get_title()
        if title.__contains__(" · Global Voices 日本語"):
            title = title.replace(" · Global Voices 日本語", "")

        news_list.append({
            'title': title,
            'content': crawler.get_text(),
            'url': crawler.get_url(),
            'published_at': crawler.get_publish_date(),
            'image_url': crawler.get_top_image(),
            'authors': ', '.join(crawler.get_authors()),
            'language': language,
            "publisher": crawler.get_publisher(),
            'access_level': 'public',
            'category': 'NEWS'
        })
    # # 3. 데이터베이스 연결하기
    # db = Databases()
    press_db_service = PressDbService(nlp_model)
    # 4. 스크래핑한 데이터를 데이터베이스에 저장하기
    for news in news_list:
        # 뉴스 컨텐츠가 두줄씩 띄어쓰기 되어있는 경우 한줄로 합치기
        news['content'] = news['content'].replace('\n\n', '\n')
        press_db_service.uploadPressDB(news['title'], news['content'], news['url'], news['published_at'],
                                       news['image_url'], news['authors'], news['language'], news['publisher'],
                                       news['access_level'], news['category'])
    print(datetime.today(), '에 저장 완료')
