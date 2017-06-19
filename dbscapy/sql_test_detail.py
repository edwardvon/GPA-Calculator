# -*- coding:utf-8 -*-

import sqlite3

from dbscapy import curriculum

conn = sqlite3.connect('curriculum.db')
print("Connect to database successfully")
cur = conn.cursor()


def insert(conn, data):
    try:
        # conn.execute("INSERT INTO curriculum_index (ID,YEAR,COLLEGE_NUM,COLLEGE,NUMBER,NAME)\
        #       VALUES (?,?,?,?,?,?)",data);
        conn.execute("INSERT INTO counter_detail (ID,NUMBER,NAME,POINT,TYPE,CLASS_NUM) \
                VALUES (?,?,?,?,?,?)", data);
    except sqlite3.Error as err:
        print(err)
    return

def delete(conn, sql=''):
    if not sql=='':
        conn.execute(sql)
    else:
        a = input("Are you sure to DELETE ALL DATA ??(YES to go)")
        if not a=="YES":
            return
        conn.execute('''DELETE from curriculum''')

def select(conn, table, place="*", flag=''):
    sql = "SELECT "+place+" from "+table+flag
    data = conn.execute(sql)
    return data


# def index_restore(conn):
#     a = input("Are you sure to RESTORE CURRICULUM_INDEX?(YES to go)")
#     if not a =='YES':
#         return
conn.execute('''DROP TABLE IF EXISTS counter_detail;''')
try:
    conn.execute('''CREATE TABLE counter_detail (
        ID INT PRIMARY KEY  NOT NULL ,
        NUMBER         CHAR(8) NOT NULL,
        NAME           TEXT NOT NULL,
        POINT          FLOAT NOT NULL,
        TYPE           INT NOT NULL,
        CLASS_NUM      INT NOT NULL,
        FOREIGN KEY(CLASS_NUM) REFERENCES counter_index(NUMBER));''')
except sqlite3.Error as err:
    print(err)

def detail_refresh(conn,class_num):
    global id
    soup = curriculum.init(class_num)
    detail_list = curriculum.get_public(soup)
    for i in detail_list:
        data = [id, *i, class_num]
        id = id + 1
        # print(data)
        insert(conn,data)
    detail_list = curriculum.get_core(soup)
    for i in detail_list:
        data = [id, *i, class_num]
        id = id + 1
        # print(data)
        insert(conn, data)
    detail_list = curriculum.get_core_sel(soup)
    for i in detail_list:
        data = [id, *i, class_num]
        id = id + 1
        # print(data)
        insert(conn, data)
    conn.commit()

a = select(conn,'counter_index',place="NUMBER")
id=1
for i in a :
    detail_refresh(conn,i[0])

b = select(conn,'counter_detail')
for i in b :
    print(i)


conn.close()
