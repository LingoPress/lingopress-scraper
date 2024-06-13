import requests
import spacy
from bs4 import BeautifulSoup

need_url = "https://www.aozora.gr.jp/cards/000035/files/301_14912.html"


def scrape_website(url):
    # 웹 페이지에 요청을 보냄
    response = requests.get(url)

    # 요청이 성공했는지 확인
    if response.status_code == 200:

        response.encoding = response.apparent_encoding
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 모든 텍스트 내용 추출
        text_content = soup.get_text()

        content = text_content.replace('。', '。\n')

        nlp = spacy.load("ja_core_news_md")
        # 텍스트를 작은 청크로 분할하여 처리
        chunk_size = 10000  # 청크 크기 조정 가능
        chunks = [text_content[i:i + chunk_size] for i in range(0, len(text_content), chunk_size)]

        total_content_line = 0  # 전체 문장 수를 저장할 변수
        line_number = 1

        for chunk in chunks:
            doc = nlp(chunk)
            sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]  # 공백 제거
            total_content_line += len(sentences)
            for _, content in enumerate(sentences):
                print("line_number: ", line_number, "content: ", content)
                line_number += 1

        print("Total content lines:", total_content_line)

        # 출력 또는 원하는 다른 작업 수행
    else:
        print("Failed to retrieve the webpage.")


# 함수 호출
scrape_website(need_url)
