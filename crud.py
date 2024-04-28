from database import Databases


class CRUD(Databases):
    def insertDB(self, table, column, data):
        sql = " INSERT INTO {table}({column}) VALUES ({data}) ;".format(table=table,
                                                                        column=column, data=data)
        print("sql")
        print(sql)
        try:
            # self.cursor.execute(sql)
            self.cursor.execute(sql, (data,))
            self.db.commit()
        except Exception as e:
            print(" insert DB err ", e)

    def readDB(self, table, column):
        sql = " SELECT {column} from {table}".format(column=column, table=table)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            result = (" read DB err", e)

        return result

    def updateDB(self, table, column, value, condition):
        sql = " UPDATE {table} SET {column}='{value}' WHERE {column}='{condition}' ".format(table=table,
                                                                                            column=column,
                                                                                            value=value,
                                                                                            condition=condition)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(" update DB err", e)

    def deleteDB(self, table, condition):
        sql = " delete from {table} where {condition} ; ".format(table=table,
                                                                 condition=condition)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("delete DB err", e)

    def insertPressDB(self, title, content, original_url, published_at, image_url, total_content_line, authors,
                      language, publisher, translated_title, access_level):
        sql = ("INSERT INTO press(title, content, original_url, published_at, image_url, total_content_line, author,"
               " language, publisher, translated_title, access_level) VALUES "
               "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;")

        try:
            self.cursor.execute(sql, (
                title, content, original_url, published_at, image_url, total_content_line, authors, language, publisher,
                translated_title, access_level))
            self.db.commit()
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(" insert DB err: ", e)

    def check_exist_url(self, original_url):
        sql = "SELECT * from press where original_url = %s"
        try:
            self.cursor.execute(sql, (original_url,))
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(" read DB err: ", e)

    def insertPressContentDB(self, press_id, line_number, content, translated_content):
        sql = "INSERT INTO press_content_line(press_id, line_number, line_text, translated_line_text) VALUES (%s, %s, %s, %s);"
        try:
            self.cursor.execute(sql, (press_id, line_number, content, translated_content))
            self.db.commit()
        except Exception as e:
            print(" insert DB err: ", e)
