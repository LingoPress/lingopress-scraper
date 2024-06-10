import re
import spacy

from crud import CRUD
from deepl_translater import translate_press_content_line


class PressDbService(CRUD):
    def __init__(self, nlp_model):
        super().__init__()
        self.nlp_model = nlp_model

    def uploadPressDB(self, title, content, original_url, published_at, image_url, authors, language, publisher,
                      access_level, category):
        if self.check_exist_url(original_url):
            print(original_url, "이미 존재하는 기사입니다.")
            return



        nlp = spacy.load(self.nlp_model)
        doc = nlp(content)
        sentences = [sent.text for sent in doc.sents]
        total_content_line = len(sentences)

        # 뉴스 저장
        brief_news_content = sentences[:3]
        combined_content = ' '.join(brief_news_content)

        last_press_id = self.insertPressDB(title, combined_content, original_url, published_at, image_url,
                                           total_content_line,
                                           authors, language, publisher, access_level, category)

        print("press_id: ", last_press_id)

        translated_title_ko = translate_press_content_line(title)
        translated_title_ja = translate_press_content_line(title, "ja")

        # 한국어 제목
        self.insertDB("press_translation", "press_id, translated_title, translated_language",
                      (last_press_id, translated_title_ko, "ko"))

        # 일본어 제목
        self.insertDB("press_translation", "press_id, translated_title, translated_language",
                      (last_press_id, translated_title_ja, "ja"))

        # 뉴스 텍스트 개별 번역 및 저장
        for line_number, content in enumerate(sentences):
            # 나중에 벌크 연산 이용해보면 좋을듯
            line_number += 1
            print("press_id: ", last_press_id, "line_number: ", line_number, "content: ", content)

            self.insertPressContentDB(last_press_id, line_number, content)

        print(original_url, "업로드 완료")
