import requests
import os
import json
from bs4 import BeautifulSoup

base_url='http://scitech.people.com.cn/GB/1057/index{}.html'
def getNewsUrl(page):
    url=base_url.format(page)
    r=requests.get(url)
    r.encoding=r.apparent_encoding
    return r.text

def parseNewList(html):
    soup=BeautifulSoup(html,features="lxml")
    pageList=[]
    for item in soup.select('li'):
        itemDic={}
        itemDic['标题']=item.a.text
        urlIterm=item.a.get('href')
        if not urlIterm.startswith('http://'):
            urlIterm='http://scitech.people.com.cn/'+urlIterm
        itemDic['url']=urlIterm
        itemDic['time']=item.em.text
        pageList.append(itemDic)
    return pageList
def saveJson(dic,path,fileNAme):
    jsonDate=json.dumps(dic,indent=2,ensure_ascii=False)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+fileNAme,'w',encoding='utf-8') as f:
        f.write(jsonDate)
urlList=[]
for page in range(1,18):
    html=getNewsUrl(page)
    page=parseNewList(html)
    urlList.extend(page)
saveJson(urlList,'files/','newlist.json')
print('运行完了')
