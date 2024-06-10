from rss_based_news_scraper import rss_based_news_scraper


rss_link_list = [
    {"lang": "en", "rss": "https://globalvoices.org/feed", "nlp_model": "en_core_web_sm"},
    {"lang": "ja", "rss": "https://jp.globalvoices.org/feed", "nlp_model": "ja_core_news_md"}
]

#
for rss in rss_link_list:
    print("@@@: ", rss['lang'], "뉴스 저장 시작 --")
    rss_based_news_scraper(rss['lang'], rss['rss'])
    print("@@@: ", rss['lang'], "뉴스 저장 완료 --")

print("일본어 뉴스 저장")
