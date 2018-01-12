# coding:utf-8

import json
import codecs


from SQL import save_mysql  # 导入sql存储数据
import MySQLdb as db

class insertMysql:
    # @staticmethod
    def __init__(self):
        self.sql = save_mysql()  # 数据库保存
        self.fail_sql = []

    def get_json(self):
        json_load = codecs.open('data.json', encoding="utf-8")
        json_list = json.load(json_load)
        lens = len(json_list)
        for i in range (0,lens):
            # print (i,json_list[i])
            try:
                self.sql.save_data(json_list[i])
                print ('v:',i)
            except:
                continue
                print ('shibai:',i)
                self.fail_sql.append(json_list[i])
        print ('lens:',len(self.fail_sql))
        outfile = codecs.open('fail_insert.json', "wb", encoding="utf-8")
        file = json.dumps(self.fail_sql, outfile, ensure_ascii=False)+'\n'
        outfile.write(file)
        outfile.close()

    def main(self):
        self.get_json()

# insertMysql.main()
if __name__ == '__main__':
    insertMysql().main()


