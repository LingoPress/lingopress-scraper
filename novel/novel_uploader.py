# csv 파일 db에 올리기
import os
import sys
import novel_txt_reader

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from press_db_service import PressDbService


def novel_upload(file_path, title, authors, language):
    content = novel_txt_reader.read_txt_file(file_path)
    press = {
        'title': title,
        'content': content,
        'url': None,
        'published_at': None,
        'image_url': "",
        'authors': authors,
        'language': language,
        "publisher": "",
        'access_level': 'public',
        'category': 'NOVEL'
    }
    press_db_service = PressDbService(None)
    press_db_service.uploadPressDB(press['title'], press['content'], press['url'], press['published_at'],
                                   press['image_url'], press['authors'], press['language'], press['publisher'],
                                   press['access_level'], press['category'])


novel_upload("../novels/물고기비늘옷_ja.csv", "魚服記", "太宰治", "ja")
