#! usr/bin/env python
# -*- coding:utf-8 -*-
# author:CM
# 2017-6-17

from bs4 import BeautifulSoup
from urllib import request

def init(id):
    url = 'http://192.168.2.224/pyfa/view_pyfa_detail.asp?fid='+str(id)
    try:
        html = request.urlopen(url)
    except request.HTTPError as err:
        print(err)
    soup = BeautifulSoup(html, "lxml")
    return soup

#获取专业信息
def get_info(soup):
    global url
    name = soup.h1.string[4:-15]
    grade = url[-10:-6]
    return grade, name

#获取毕业总学分要求
def get_total(id):
    soup = init(id)
    curr_request = soup.select('#byyq_in .ncontents')
    curr_total = []
    for i in range((len(curr_request)+1)//3):
        a = curr_request[i*3:i*3+3]
        for j in range(0,3):
            a[j] = a[j].get_text().strip()
            a[j] = a[j].replace(' ','').replace('\r','').replace('\n','').replace('\t','')
        curr_total.append(a)
    return [curr_total[1][1],curr_total[2][1],curr_total[3][1],curr_total[4][1],curr_total[3][2]]

#获取公共必修内容
def get_public(soup):
    curr_request = soup.select('#fb1 .nwks .ncontents')
    curr_public = []
    for i in range((len(curr_request)+1)//17):
        a = curr_request[i*17:i*17+17]
        for j in range(0,17):
            a[j] = a[j].get_text().strip()
            a[j] = a[j].replace('\r','').replace('\n','').replace('\t','')
        a[3] = a[4]
        curr_public.append([*a[1:4],1])
    return curr_public

#获取专业核心课内容
def get_core(soup):
    curr_request = soup.select('#fb2 .nwks .ncontents')
    curr_core = []
    for i in range((len(curr_request)+1)//17):
        a = curr_request[i*17:i*17+17]
        for j in range(0,17):
            a[j] = a[j].get_text().strip()
            a[j] = a[j].replace('\r','').replace('\n','').replace('\t','')
        a[3] = a[4]
        curr_core.append([*a[1:4],2])
    return curr_core

#获取专业选修课内容
def get_core_sel(soup):
    curr_request = soup.select('#fb3 .nwks .ncontents')
    curr_core_sel = []
    for i in range((len(curr_request)+1)//17):
        a = curr_request[i*17:i*17+17]
        for j in range(0,17):
            a[j] = a[j].get_text().strip()
            a[j] = a[j].replace('\r','').replace('\n','').replace('\t','')
        a[3] = a[4]
        curr_core_sel.append([*a[1:4],3])
    return curr_core_sel

# def
if __name__ == "__main__":
    soup=init(2014172000)
    print(get_core_sel(soup))