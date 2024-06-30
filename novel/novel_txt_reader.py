import csv


# csv 파일을 읽어서 출력하는 함수
def read_txt_file(txt_filename):
    lines = []
    with open(txt_filename, mode='r', encoding='utf-8') as txt_file:
        for line in txt_file:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.isspace():
                lines.append(stripped_line)
    return lines

# 함수 호출
read_txt_file("../novels/잭과콩나무_en.csv")
