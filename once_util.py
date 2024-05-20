from crud import CRUD
from deepl_translater import translate_press_content_line


#  ko 타입으로 된 press_translation 테이블을 조회해서 일본어로 번역해서 ja 타입으로 저장하기
def update_press_translation():
    crud = CRUD()
    data = crud.readDB("press_translation", "id, press_id, translated_title, translated_language")
    for line in data:
        press_id = line[1]
        translated_title = line[2]
        translated_language = line[3]
        if translated_language == "ko":
            translated_title = translate_press_content_line(translated_title, "ja")
            crud.insertDB("press_translation", "press_id, translated_title, translated_language", (press_id, translated_title, "ja"))


update_press_translation()