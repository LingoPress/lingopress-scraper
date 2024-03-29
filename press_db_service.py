from crud import CRUD
from deepl_translater import translate_press_content_line


class PressDbService(CRUD):

    def uploadPressDB(self, title, content, original_url, published_at, image_url, total_content_line):
        if self.check_exist_url(original_url):
            print(original_url, "이미 존재하는 기사입니다.")
            return

        # 뉴스 저장
        last_press_id = self.insertPressDB(title, content, original_url, published_at, image_url, total_content_line)
        print("press_id: ", last_press_id)

        # 뉴스 텍스트 리스트로 분리
        content_list = content.split('\n')

        # 뉴스 텍스트 개별 번역 및 저장
        for line_number, content in enumerate(content_list):
            # 나중에 벌크 연산 이용해보면 좋을듯
            if len(content) == 0:
                continue
            line_number += 1
            print("press_id: ", last_press_id, "line_number: ", line_number, "content: ", content)
            translated_content = translate_press_content_line(content)
            self.insertPressContentDB(last_press_id, line_number, content, translated_content)

        print(original_url, "업로드 완료")




