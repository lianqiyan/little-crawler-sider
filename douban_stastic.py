import requests
from bs4 import BeautifulSoup
import re
import operator
import rpy2.robjects as robjects
import numpy as np
import pandas as pd
from rpy2.robjects.lib import ggplot2
from rpy2.robjects import pandas2ri
pandas2ri.activate()
from rpy2.robjects.packages import importr


def get_info(url, score, year, country, class_a):
    html_t = requests.get(url).text
    soup_t = BeautifulSoup(html_t, 'html.parser')
    # title_h = soup_t.findAll('span', {'class': 'title'})
    score_h = soup_t.findAll('span', {'class': 'rating_num'})
    p_h = soup_t.findAll('br')

    # print(title_h)
    for i in range(0, (len(p_h))):
        temp = p_h[i].text.strip().split(' / ')
        year_t = temp[0]
        class_t = temp[2]
        class_a.append(class_t)
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
    for key, value in sorted(w_dic.items(), key=operator.itemgetter(1)):
        print(key, value)
    return w_dic


def get_category(data):
    c_dic = {}
    for c in data:
        c = c.split(' ')
        for cc in c:
            if cc in c_dic:
                c_dic[cc] += 1
            else:
                c_dic[cc] = 1
    for key, value in sorted(c_dic.items(), key=operator.itemgetter(1)):
        print(key, value)
    return c_dic


# title = []
score = []
year = []
country = []
class_a = []

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
    get_info(url, score, year, country, class_a)

a_num = get_category(class_a)
c_num = create_dic(country)
y_num = create_dic(year)
s_country = list(c_num.keys())
sc_n = list(c_num.values())
s_year = list(y_num.keys())
sy_n = list(y_num.values())
s_class = list(a_num.keys())
sa_n = list(a_num.values())
index = sorted(range(len(s_year)), key=lambda k: s_year[k])
temp1 = []
temp2 = []
for i in index:
    temp1.append(s_year[i])
    temp2.append(sy_n[i])
s_year = temp1
sy_n = temp2


color = list(np.random.normal(0, 20, len(sc_n)))
colory = list(np.random.uniform(0, 80, len(s_year)))
colora = list(np.random.uniform(0, 80, len(s_class)))

df = pd.DataFrame({'Country': s_country,
                   'Number': sc_n,
                   'Color': color})
rdf = pandas2ri.py2ri(df)
yf = pd.DataFrame({'Year': s_year,
                   'Number': sy_n,
                   'Color': colory})
ryf = pandas2ri.py2ri(yf)
af = pd.DataFrame({'Species': s_class,
                   'Number': sa_n,
                   'Color': colora})
raf = pandas2ri.py2ri(af)
spe = len(sc_n)*['Country'] + len(sy_n)*['Year'] + len(sa_n)*['Species']
nu = sc_n + sy_n + sa_n
colors = list(np.random.uniform(0, 80, len(nu)))
colr = len(sc_n)*[3] + len(sy_n)*[7] + len(sa_n)*[5]
nf = pd.DataFrame({'Species': spe,
                   'Number': nu,
                   'ColorR': colr,
                   'Color': colors})
rnf = pandas2ri.py2ri(nf)

grdevices = importr('grDevices')
grdevices.png(file="E:/python code/crawler/file.png", width=1024, height=720)
pp = ggplot2.ggplot(rdf) + \
     ggplot2.aes_string(x='Country', y='Number', fill='Country') + \
     ggplot2.geom_bar(stat="identity") + \
     ggplot2.ggtitle('The Number of Movies in Countries')
pp.plot()

grdevices.png(file="E:/python code/crawler/file4.png", width=1024, height=720)
gg = ggplot2.ggplot(raf) + \
     ggplot2.aes_string(x='Species', y='Number', fill='Species') + \
     ggplot2.geom_bar(stat="identity") + \
     ggplot2.ggtitle('The Number of Movies in Species')
gg.plot()

grdevices.png(file="E:/python code/crawler/file2.png", width=1400, height=720)
gp = ggplot2.ggplot(ryf)

pp = gp + \
     ggplot2.aes_string(x='Year', y='Number', group=1, col='Color') + \
     ggplot2.geom_point(stat="identity", colour="grey50", size=5.5) + \
     ggplot2.geom_point(size=5) + \
     ggplot2.geom_line() + \
     ggplot2.ggtitle('The Number of Movies in Years')
pp.plot()
grdevices.png(file="E:/python code/crawler/file3.png", width=1024, height=540)
ss = ggplot2.ggplot(rnf) + \
     ggplot2.aes_string(x='Species', y='Number', col='Color') + \
     ggplot2.geom_boxplot(fill=robjects.FloatVector([3, 5, 7])) +\
     ggplot2.geom_jitter(width=0.2) +\
     ggplot2.ggtitle('The Boxplot of Movies in Different Index')
ss.plot()
