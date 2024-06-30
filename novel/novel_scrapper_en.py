import os
import sys
import csv
import spacy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from press_scraper import PressScraper

need_url = "https://americanliterature.com/author/f-scott-fitzgerald/book/the-great-gatsby/chapter-1"

def scrape_website(url, txt_filename):
    crawler = PressScraper(url, "en")
    print(crawler.get_title())
    text_content = crawler.get_text()
    nlp = spacy.load("en_core_web_sm")

    chunk_size = 10000  # 청크 크기 조정 가능
    chunks = [text_content[i:i + chunk_size] for i in range(0, len(text_content), chunk_size)]
    upload_content = []
    line_number = 1
    total_content_line = 0
    # CSV 파일 작성
    with open(txt_filename, mode='w', encoding='utf-8') as txt_file:
        for chunk in chunks:
            doc = nlp(chunk)
            sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]  # 공백 제거
            total_content_line += len(sentences)
            for _, content in enumerate(sentences):
                # 빈칸이나 공백이 아닌 경우에만 추가
                if content and not content.isspace():
                    upload_content.append(content)
                    print("line_number: ", line_number, "content: ", content)
                    # 텍스트 파일에 행 추가
                    txt_file.write(content + '\n')
                    line_number += 1

    print("Total content lines:", total_content_line)

scrape_website(need_url, "../novels/위대한개츠비1_en.csv")