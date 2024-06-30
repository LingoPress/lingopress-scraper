import csv


# csv 파일을 읽어서 출력하는 함수
def read_csv_file(csv_filename):
    list = []
    with open(csv_filename, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row and not row[0].isspace():
                list.append(row[0])

    return list


# 함수 호출
read_csv_file("../novels/인간실격_ja.csv")
