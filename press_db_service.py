import re

from crud import CRUD
from deepl_translater import translate_press_content_line


class PressDbService(CRUD):

    def uploadPressDB(self, title, content, original_url, published_at, image_url, authors, language, publisher,
                      access_level):
        if self.check_exist_url(original_url):
            print(original_url, "이미 존재하는 기사입니다.")
            return

        translated_title = translate_press_content_line(title)

        # 뉴스 텍스트 리스트로 분리
        content_list = content.split('\n')
        # 각 라인의 길이가 0이거나 '﻿'인 경우 제외
        filtered_content_list = [c for c in content_list if len(c) > 0 and c != '﻿']
        # 각 라인 끝에 구분자 추가
        content_list = [c + '!@!' for c in filtered_content_list]
        # 각 라인을 ". " 단위 리스트로 분리
        separated_content_list = [re.split(r'(?<=\.)\s+', c) for c in content_list]
        # 이중 리스트를 다시 1차원 리스트로 변환
        separated_content_list = [item for sublist in separated_content_list for item in sublist]

        total_content_line = len(separated_content_list)

        # 뉴스 저장
        last_press_id = self.insertPressDB(title, content, original_url, published_at, image_url, total_content_line,
                                           authors, language, publisher, translated_title, access_level)
        print("press_id: ", last_press_id)

        # 뉴스 텍스트 개별 번역 및 저장
        for line_number, content in enumerate(separated_content_list):
            # 나중에 벌크 연산 이용해보면 좋을듯
            line_number += 1
            print("press_id: ", last_press_id, "line_number: ", line_number, "content: ", content)
            if content.__contains__('!@!'):
                removed = content.replace('!@!', '')
                translated_content = translate_press_content_line(removed)
                self.insertPressContentDB(last_press_id, line_number, content, translated_content)
                continue
            translated_content = translate_press_content_line(content)

            self.insertPressContentDB(last_press_id, line_number, content, translated_content)

        print(original_url, "업로드 완료")
