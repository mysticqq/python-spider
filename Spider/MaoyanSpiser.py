import requests
import re
import pymongo

MONGO_URL='localhost'#
MONGO_DB='Maoyan'
MONGO_TABLE='MoviesTop100'

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

def save_to_mongo(info):
    if db[MONGO_TABLE].insert(info):
        print('保存成功',info)
    else:
        print('保存失败',info)

def get_one_page(url):
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    html = requests.get(url=url,headers=headers).text
    return html

def get_movies_info(html):
    pattern=re.compile('<dd>.*?title="(.*?)".*?<p.*?star.*?>(.*?)</p>.*?<p.*?releasetime.*?>(.*?)</p>.*?<i.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>',re.S)
    results = re.findall(pattern,html)
    for result in results:
        movies = {}
        movies['name']=result[0]
        movies['actor']=result[1].strip()[3:]
        movies['time']=result[2].strip()[5:]
        movies['rate']=result[3]+result[4]
        save_to_mongo(movies)

#主体函数
def main():
    for i in range(10):
        url = 'http://maoyan.com/board/4?offset='+str(i*10)
        html=get_one_page(url)#完成请求，获取响应体的超文本
        get_movies_info(html)#完成信息提取

if __name__=='__main__':
    main()