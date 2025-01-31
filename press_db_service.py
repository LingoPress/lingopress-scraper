import re
import spacy
from crud import CRUD
from deepl_translater import translate_press_content_line


class PressDbService(CRUD):
    def __init__(self, nlp_model):
        super().__init__()
        if nlp_model is not None:
            self.nlp_model = nlp_model

    def uploadPressDB(self, title, content, original_url, published_at, image_url, authors, language, publisher,
                      access_level, category):
        if self.check_exist_url(original_url):
            print(original_url, "이미 존재하는 기사입니다.")
            return

        combined_content = ""
        total_content_line = 0
        if category == "NEWS":
            nlp = spacy.load(self.nlp_model)
            doc = nlp(content)
            content = [sent.text for sent in doc.sents]
            total_content_line = len(content)
            # 뉴스 저장
            brief_news_content = content[:3]
            combined_content = ' '.join(brief_news_content)
        if category == "NOVEL":
            total_content_line = len(content)
            combined_content = ""

        last_press_id = self.insertPressDB(title, combined_content, original_url, published_at, image_url,
                                           total_content_line,
                                           authors, language, publisher, access_level, category)

        print("press_id: ", last_press_id)

        # TODO: 원문 언어를 제외한 언어로 제목 번역
        print("@@@@@ lang", language)

        support_language_list = ["ko", "ja", "en"]
        support_language_list.remove(language)
        for target_lang in support_language_list:
            translated_title = translate_press_content_line(title, target_lang)
            self.insertDB("press_translation", "press_id, translated_title, translated_language",
                          (last_press_id, translated_title, target_lang))
        # translated_title_ko = translate_press_content_line(title)
        # translated_title_ja = translate_press_content_line(title, "ja")

        # 한국어 제목
        # self.insertDB("press_translation", "press_id, translated_title, translated_language",
        #              (last_press_id, translated_title_ko, "ko"))

        # 일본어 제목
        # self.insertDB("press_translation", "press_id, translated_title, translated_language",
        #              (last_press_id, translated_title_ja, "ja"))

        # 뉴스 텍스트 개별 번역 및 저장
        for line_number, content_line in enumerate(content):
            # 나중에 벌크 연산 이용해보면 좋을듯
            line_number += 1
            print("press_id: ", last_press_id, "line_number: ", line_number, "content: ", content_line)

            self.insertPressContentDB(last_press_id, line_number, content_line)

        print(original_url, "업로드 완료")
