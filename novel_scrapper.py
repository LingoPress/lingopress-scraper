import spacy

from press_scraper import PressScraper

need_url = "https://www.aozora.gr.jp/cards/000035/files/301_14912.html"
crawler = PressScraper(need_url)
print(crawler.get_title())
content = crawler.get_text()
nlp = spacy.load("ja_core_news_md")
doc = nlp(content)
sentences = [sent.text for sent in doc.sents]
total_content_line = len(sentences)

print(sentences)
print(total_content_line)