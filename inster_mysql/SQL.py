# coding:utf-8
import MySQLdb as db
import json
import codecs


# 将得到的数据存入数据库中mysql
class save_mysql:
    def __init__(self):
        self.user = 'root'
        self.password = 'root'
        self.host = 'localhost'
        self.database = 'data_12'
        self.list = ['profile','unApply','DC','specification','Titanic','Jtype','tname','ltime','usage','applyPeople',
                     'taboo','care','nutritionAnalysis','pname','yname',]
        self.n = 0
        # self.fail_sql = []

    def get_connection(self):
        return db.connect(user="root", passwd="123456", host="localhost", db="test_39", charset="utf8")

    def save_data(self, data_sv):
        conn = self.get_connection()
        cursor = conn.cursor()
        data = {}
        for i in self.list:
            try:
                data[i] = data_sv[i]
            except:
                data[i] = None
        sql = "INSERT INTO data_12(profile,unApply,DC,specification,Titanic,Jtype,tname,ltime,applyPeople,usages,taboo,care,nutritionAnalysis,pname,yname) \
              VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (data['profile'], data['unApply'], data['DC'], data['specification'], data['Titanic'], data['Jtype'],data['tname'], data['ltime'], data['applyPeople'], data['usage'], data['taboo'], data['care'],data['nutritionAnalysis'], data['pname'],data['yname'])
        # print ('sql:',sql)
        # import pdb;pdb.set_trace()
        try:
            # print ('sql:',sql)
            cursor.execute(sql)  # 将data插入到数据库中
            conn.commit()
        except:
            conn.rollback()
            self.n = self.n +1
            print ('shibai:',self.n)
            self.fail_sql.append(data)
        # cursor.close()
        # conn.close()
