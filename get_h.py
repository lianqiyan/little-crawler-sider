from requests import session
from bs4 import BeautifulSoup
import re


def get_img(page_link):
    all = []
    for link in page_link:
        print(link)
        r_p = c.get(link, cookies=cook).content
        p_html = BeautifulSoup(r_p, 'html.parser')
        s_m = p_html.findAll('a', {'href': re.compile("http://weibo\.cn/mblog/oripic\?[&0-9A-Za-z=\-?]+")})
        a_m = p_html.findAll('a', {'href': re.compile("http://weibo\.cn/mblog/picAll/[&0-9A-Za-z=\-?]+")})
        # print(a_m)
        # print(s_m)
        s_mm = []
        for t1 in s_m:
            t1 = t1["href"]
            s_mm.append(t1)
        for t2 in a_m:
            a_p = c.get(t2["href"], cookies=cook).content
            # print(a_p)
            a_html = BeautifulSoup(a_p, 'html.parser')
            ss_m = a_html.findAll('a', {'href': re.compile("/mblog/oripic\?[&0-9A-Za-z=\-?]+")})
            for t22 in ss_m:
                t22 = t22["href"]
                t22 = 'http://weibo.cn' + t22
                s_mm.append(t22)
            all.extend(s_mm)
    clea = clean(all)
    return clea


def clean(t_link):
    cle = []
    for t in t_link:
        if t in cle:
            continue
        else:
            print(t)
            cle.append(t)
    return cle

        # http://ww2.sinaimg.cn/large/7c9b551fgw1f4ij3retffj20k20qon07.jpg
url = "http://weibo.cn/u/2090554655?filter=1"
cook = dict(cookies='your cookies')
with session() as c:
    response = c.get(url, cookies=cook).content
    Bo = BeautifulSoup(response, "html.parser")
    page_de = Bo.find('input', {'type': 'submit'}).nextSibling
    page = page_de[3:5]
    # c_link = get_img(url)
    pa_link = []
    for n in range(1, int(page) + 1):
        if n is 1:
            temp = url
            pa_link.append(temp)
        else:
            temp = url + '&page=' + str(n)
            pa_link.append(temp)
    c_link = get_img(pa_link)
    x = 1
    for i in c_link:
        bin = c.get(i, cookies=cook).content
        with open('E:/python code/data_control/%s.jpg' % x, 'wb') as file:
            file.write(bin)
            x += 1


    # s_m = Bo.findAll('a', {'href': re.compile("http://weibo\.cn/mblog/oripic\?[&0-9A-Za-z=\-?]+")})
    # a_m = Bo.findAll('a', {'href': re.compile("http://weibo\.cn/mblog/picAll/[&0-9A-Za-z=\-?]+")})
    # print(a_m)
