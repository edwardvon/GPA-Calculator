from bs4 import BeautifulSoup
from urllib import request


url = 'http://192.168.2.224/pyfa/view_pyfa_detail.asp?fid='+str(id)
try:
    html = request.urlopen(url)
except request.HTTPError as err:
    print(err)
soup = BeautifulSoup(html, "lxml")
