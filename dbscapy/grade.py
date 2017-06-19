# grade.py
#! usr/bin/env python
# -*- coding:UTF-8 -*-
import re
import json

#def list2json()

with open("data1.txt","rb") as f:
    head= f.readline().decode().split("\t")
    head= head[0][-2:]
    print(head)
    print(head[0] == u"学号")
    save = open("sec1.txt", "w",encoding="UTF-8")
    for line in f.readlines():
        a = line.decode().split("\t")
        if re.match(r"\d{1,2}(?!\S)", a[0]):
            lined = ''
            for i in a:
                lined = lined + i + " "
            lined = lined + "\n"
            save.write(lined)
    save.close()
