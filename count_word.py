import requests
from bs4 import BeautifulSoup
import operator


def get_word(url):
    html = requests.get(url).text
    word_list = []
    soup = BeautifulSoup(html, 'html.parser')
    iid = ["why-python", "scientific-python-building-blocks", "the-interactive-workflow-ipython-and-a-text-editor"]
    for d in iid:
        for i in soup.findAll('div', {'class': 'section', 'id': d}):
            # print(i.text)
            content = i.text
            words = content.lower().split()
            for w in words:
                # print(w)
                word_list.append(w)
    clean_word(word_list)


def clean_word(word_list):
    cleanlist = []
    symbol = '-|“”.’,;~@!#$%^&*()_+:"?><\'[]+{}'
    for word in word_list:
        for c in symbol:
            word = word.replace(c, '')
        if len(word) > 0:
            cleanlist.append(word)
    create_dic(cleanlist)
    print(cleanlist[len(cleanlist) - 1])


def create_dic(cleanlist):
    w_dic = {}
    for word in cleanlist:
        if word in w_dic:
            w_dic[word] +=1
        else:
            w_dic[word] = 1
    for key, value in sorted(w_dic.items(), key=operator.itemgetter(1)):
        print(key, value)


get_word('http://www.scipy-lectures.org/intro/intro.html')
