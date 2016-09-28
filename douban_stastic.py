import requests
import numpy as np
from bs4 import BeautifulSoup
import re
import operator


def get_info(url, score, year, country):
    html_t = requests.get(url).text
    soup_t = BeautifulSoup(html_t, 'html.parser')
    # title_h = soup_t.findAll('span', {'class': 'title'})
    score_h = soup_t.findAll('span', {'class': 'rating_num'})
    p_h = soup_t.findAll('br')

    # print(title_h)
    for i in range(0, (len(p_h))):
        temp = p_h[i].text.strip().split(' / ')
        year_t = temp[0]
        t = temp[1]
        country_t = t[0:3]
        year.append(year_t)
        country.append(country_t.strip())

    for i in range(0, (len(score_h))):
        score.append(float(score_h[i].text))


def create_dic(country):
    w_dic = {}
    for word in country:
        if word in w_dic:
            w_dic[word] += 1
        else:
            w_dic[word] = 1
    for key, value in sorted(w_dic.items(), key=operator.itemgetter(1)):
        print(key, value)


# title = []
score = []
year = []
country = []

html = requests.get('https://movie.douban.com/top250').text
soup = BeautifulSoup(html, 'html.parser')
next = soup.findAll('a', {'href': re.compile("\?start=25&filter=$")})
temp = next[0]["href"]
front = temp[0:7]
end = temp[9:]
normal = 'https://movie.douban.com/top250'

for i in range(0, 10):
    if i is 0:
        url = normal
    else:
        url = normal + front + str(i*25) + end
    get_info(url, score, year, country)

# print(score)
create_dic(country)
# print(country[-1],country[-2])
# for i in range(0, len(score) - 1):
#     print(score[i])
#     print(country[i])
#     print(year[i])
