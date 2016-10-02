import requests
from bs4 import BeautifulSoup
import re
import operator
import numpy as np
import pandas as pd
from rpy2.robjects.lib import ggplot2
from rpy2.robjects import pandas2ri
pandas2ri.activate()


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
        if len(year_t) > 4:
            year_t = year_t[0:4]
        t = temp[1]
        country_t = t[0:3]
        year.append(year_t)
        country.append(country_t.strip())

    for i in range(0, (len(score_h))):
        score.append(float(score_h[i].text))


def create_dic(label):
    w_dic = {}
    for word in label:
        if word in w_dic:
            w_dic[word] += 1
        else:
            w_dic[word] = 1
    # for key, value in sorted(w_dic.items(), key=operator.itemgetter(1)):
    #     print(key, value)
    return w_dic


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
del temp

for i in range(0, 10):
    if i is 0:
        url = normal
    else:
        url = normal + front + str(i*25) + end
    get_info(url, score, year, country)


c_num = create_dic(country)
y_num = create_dic(year)
s_country = list(c_num.keys())
sc_n = list(c_num.values())
s_year = list(y_num.keys())
sy_n = list(y_num.values())
index = sorted(range(len(s_year)), key=lambda k: s_year[k])
temp1 = []
temp2 = []
for i in index:
    temp1.append(s_year[i])
    temp2.append(sy_n[i])
s_year = temp1
sy_n = temp2
del temp1, temp2
color = list(np.random.normal(20, 20, len(sc_n)))

colory = np.random.normal(30, 20, len(s_year))

df = pd.DataFrame({'country': s_country,
                   'number': sc_n,
                   'color': color})
rdf = pandas2ri.py2ri(df)

yf = pd.DataFrame({'year': s_year,
                   'number': sy_n,
                   'color': colory})
ryf = pandas2ri.py2ri(yf)
# print(type(rdf))


pp = ggplot2.ggplot(rdf) + \
     ggplot2.aes_string(x='country', y='number', fill='color') + \
     ggplot2.geom_bar(stat="identity")
pp.plot()


gp = ggplot2.ggplot(ryf)

pp = gp + \
     ggplot2.aes_string(x='year', y='number', group=1, col='color') + \
     ggplot2.geom_point(colour="grey50", size=4) + \
     ggplot2.geom_point(size=2.5) + \
     ggplot2.geom_line() 
pp.plot()



vv = ggplot2.ggplot(rdf) + \
     ggplot2.aes_string(x='country', fill='factor(color)') +\
     ggplot2.geom_bar(width=1) +\
     ggplot2.coord_polar(theta='number')
vv.plot()


