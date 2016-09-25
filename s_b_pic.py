from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import re

url = "http://www.uumnt.com/xinggan/5041.html"


m_html = "http://www.uumnt.com"
html = urlopen(url)
imObj = BeautifulSoup(html.read(), "html.parser")
image_link = imObj.findAll("a", {"href": re.compile("\/xinggan\/[0-9]*\_[0-9]*\.html")})
print(image_link[-1]["href"][14:16])
f_html = image_link[-1]["href"][0:14]
page = image_link[-1]["href"][14:16]
print(f_html)

for i in range(0, int(page) - 1):
    # i = i+56
    if i is 0:
        link = m_html + image_link[-1]["href"][0:13] + '.html'
    else:
        link = m_html + f_html + str(i) + '.html'
    print(link)
    html_inside = urlopen(link)
    imObj = BeautifulSoup(html_inside.read(), "html.parser")
    image = imObj.findAll("img", {
        "src": re.compile("http\:\/\/imgnew\.uumnt\.cc\:[0-9]*\/Pics\/2016/[0-9]*/[0-9]*/[0-9]*.jpg$")})
    print(image[0]["src"])
    if i is 0:
        full_name = str(i+1) + ".jpg"
    else:
        full_name = str(i) + ".jpg"
    urllib.request.urlretrieve(image[0]["src"], full_name)
print("OK!")
