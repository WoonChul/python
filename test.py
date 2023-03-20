import tkinter as tk
import os,math
import pymysql
from tkinter import ttk
from genInit import *

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='sql_db', charset='utf8')
# 커서 가져오기
cursor = db.cursor()

# SQL 문 만들기
#sql = '''
#     CREATE TABLE korea2 (
#     id INT UNSIGNED NOT NULL AUTO_INCREMENT,
#     name VARCHAR(20) NOT NULL,
#     model_num VARCHAR(10) NOT NULL,
#     model_type VARCHAR(10) NOT NULL,
#     PRIMARY KEY(id)
#     );
#     '''
#
# 실행하기
sql = "select emp_id,ename from sql_db.emp"
cursor.execute(sql)
result = cursor.fetchall()
# DB에 Complete 하기
#db.commit()
# DB 연결 닫기
db.close()
for row_data in result:
       print(row_data)

"""
root = tk.Tk()
root.title("Test")
root.geometry("300x790")
root.resizable(False, False)

frame = ttk.Frame(root)
test_label = ttk.Label(frame,text = "TEST")
test_label.pack()


root.mainloop()

g = Gen()

JOB = os.environ["JOB"]
STEP = os.environ["STEP"]
print(JOB)
print(STEP)

print(len(g.DO_INFO(F"-t layer -e {JOB}/{STEP}/ss -d FEATURES -o select")))


m2 = GeoMetry()

poly = [5,5,10,15,25,15,40,20,45,15,45,5,35,5,15,10,10,5]

a = m2.pointInsidePolygon([30,10],poly)

print(a)

"""