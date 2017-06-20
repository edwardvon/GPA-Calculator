# -*- coding:utf-8 -*-

import sqlite3

from dbscapy import curriculum_index

conn = sqlite3.connect('curriculum.db')
print("Connect to database successfully")
cur = conn.cursor()


def insert(conn, data):
    try:
        # conn.execute("INSERT INTO curriculum_index (ID,YEAR,COLLEGE_NUM,COLLEGE,NUMBER,NAME)\
        #       VALUES (?,?,?,?,?,?)",data);
        conn.execute("INSERT INTO counter_index (COLLEGE_NUM,YEAR,COLLEGE,NUMBER,NAME,SCORE_PUB,  \
                    SCORE_CORE,SCORE_SELE,SCORE_DEV,PS) VALUES (?,?,?,?,?,?,?,?,?,?)", data);
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

def select(conn, table, flag=''):
    # sql = 'SELECT * from counter_index WHERE college = "光电工程学院";'
    data = conn.execute("""SELECT * from counter_index WHERE college = "光电工程学院";""")
    return data


# def index_restore(conn):
#     a = input("Are you sure to RESTORE CURRICULUM_INDEX?(YES to go)")
#     if not a =='YES':
#         return
# conn.execute('''DROP TABLE IF EXISTS counter_index;''')
# try:
#     conn.execute('''CREATE TABLE counter_index (
#         COLLEGE_NUM           INT  NOT NULL ,
#         YEAR    INT  NOT NULL ,
#         COLLEGE        TEXT NOT NULL ,
#         NUMBER         INT PRIMARY KEY NOT NULL,
#         NAME           TEXT NOT NULL,
#         SCORE_PUB      FLOAT NOT NULL,
#         SCORE_CORE     FLOAT NOT NULL,
#         SCORE_SELE     FLOAT NOT NULL,
#         SCORE_DEV      FLOAT NOT NULL,
#         PS             TEXT);''')
# except sqlite3.Error as err:
#     print(err)

def index_refresh(conn):
    for year in [2013,2014,2015,2016]:
        for college in range(1,31):
            soup = curriculum_index.init(year, college)
            college_list = curriculum_index.get_index(soup)
            for i in college_list:
                data = [college, year, *i]
                # print(data)
                insert(conn,data)
    conn.commit()

# index_refresh(conn)
a = select(conn,'counter_index')
for i in a :
    print(i)

conn.close()
