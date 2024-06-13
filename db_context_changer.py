# db에 기존 구분자로 사용했던 "!@!" 대신 "\n"으로 변경하였기에, 기존 항목들을 alter table로 수정해야 합니다.
# line_text 컬럼에서 "!@!"를 "\n"으로 변경, translated_line_text 컬럼의 마지막에 "\n" 붙이기
# Path: db_context_changer.py
import crud


crud = crud.CRUD()

# line_text 컬럼에서 "!@!"를 "\n"으로 변경
def update_press_content():
    data = crud.selectPressContentLine()
    for line in data:
        line_id = line[0]
        line_text = line[1]
        line_text = line_text.replace("!@!", "\n")
        crud.updatePressContentLine(line_id, line_text)
        print(line_id, "번 데이터 수정 완료")

