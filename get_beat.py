from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import re


def get_link(main):
    html = urlopen(main)
    imObj = BeautifulSoup(html.read(), "html.parser")
    image_link = imObj.findAll("a", {"class": "img_album_btn"})
    return image_link

def get_page(p_link):
    html2 = urlopen(p_link)
    imObj2 = BeautifulSoup(html2.read(), "html.parser")
    page = imObj2.findAll('div', {'class': 'pages'})
    temp = page[0].text.strip()
    page = temp.split('共')
    temp = page[1]
    page = temp.split('页')
    page = page[0]
    return page

def download_img(tt):
    html3 = urlopen(tt)
    imObj3 = BeautifulSoup(html3.read(), "html.parser")
    m_link = imObj3.findAll('img', {'src':
    re.compile("/uploads/allimg/[0-9A-Za_z/_-]+\.jpg$")}) #/uploads/allimg/160610/1-160610143Z8.jpg
    temp = (m_link[0]["src"])
    imh = m_html + temp
    return imh

url = "http://www.eouok.com.cn/a/toupai/"
m_html = 'http://www.eouok.com.cn'
link = get_link(url)
ii = 0
for i in link:
    temp = i["href"]
    to_go = m_html + temp
    page = get_page(to_go)
    ii +=1
    for j in range(0, int(page)-1):
        if j is 0:
            to = to_go
            print(to)
            kk = download_img(to)
            print(kk)
            name = str(ii) + '0' + str(j + 1) + '.jpg'
            urllib.request.urlretrieve(kk, name)
        else:
            to = to_go.split('.html')
            to = to[0] + '_' + str(j + 1) + '.html'
            print(to)
            kk = download_img(to)
            print(kk)
            name = str(ii) + '0' + str(j + 1) + '.jpg'
            urllib.request.urlretrieve(kk, name)
