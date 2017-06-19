#! usr/bin/env python
# -*- coding:utf-8 -*-
# author:CM
# 2017-6-17

from urllib import request

from bs4 import BeautifulSoup

from dbscapy import curriculum


def init(year,college):
    if college < 10:
        college = '0'+str(college)
    url = 'http://192.168.2.224/pyfa/view_pyfa.asp?nj='+str(year)+'&xydh='+str(college)
    try:
        html = request.urlopen(url)
    except request.HTTPError as err:
        print(err)
    soup = BeautifulSoup(html, "lxml")
    return soup


#获取专业索引
#返回 学院 专业码 专业名称
def get_index(soup):
    curr_request = soup.select('.ncontents')
    curr_total = []
    for i in curr_request:
        index = i.a.string.strip().split('，')
        index[1]=i.a['href'][-10:]
        score = curriculum.get_total(index[1])
        for j in score:
            index.append(j)
        curr_total.append(index)
    return curr_total



if __name__ == "__main__":
    soup = init(2014,17)
    print(get_index(soup))
