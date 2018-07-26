from urllib import request
from urllib import parse
from urllib.error import URLError
import json
import math
import pymongo


MONGO_URL='localhost'
MONGO_DB='LaGou'
MONGO_TABLE='数据分析'

client = pymongo.MongoClient(MONGO_URL)#连接数据库
db=client[MONGO_DB]#创建数据库的名字

page=0#页码信息
City='深圳'
KeyWord='数据分析师'
base_url='https://www.lagou.com/jobs/positionAjax.json?'
params = {
    'px':'default',
    'city':City,
    'needAddtionalResult':'false'
}
url = base_url+parse.urlencode(params)
headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':64,
    'Cookie':'_ga=GA1.2.257516341.1522050452; user_trace_token=20180326154732-f0f5196c-30c9-11e8-9f49-525400f775ce; LGUID=20180326154732-f0f520df-30c9-11e8-9f49-525400f775ce; LG_LOGIN_USER_ID=60032b76bd32a5a6a596559eade6d0052f15fc2ab9779cc8; index_location_city=%E6%B7%B1%E5%9C%B3; JSESSIONID=ABAAABAAAIAACBI1A73582AEDC2FDC8335E968502A9F5D2; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527150390,1528277552,1528789503,1529461642; _gid=GA1.2.1084200828.1529461642; LGSID=20180620153431-5f3689a6-745c-11e8-aa10-525400f775ce; TG-TRACK-CODE=search_code; LGRID=20180620160449-9a8ba121-7460-11e8-aa14-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1529481888; SEARCH_ID=efa038bbf91d47488b5c710088432205',
    'Host':'www.lagou.com',
    'Origin':'https://www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88?px=default&city=%E6%B7%B1%E5%9C%B3',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

#请求和获取信息的函数
def get_postion_info(pn=1):
    global page#全局的页码
    data = {
        'first':'true',
        'pn':pn,
        'kd':KeyWord
    }
    try:
        data = bytes(parse.urlencode(data),encoding='utf-8')
        req = request.Request(url=url,data=data,headers=headers,method='POST')#构建Request对象
        html = request.urlopen(req)#发送请求
        if html.status==200:
            html = html.read().decode('utf-8')#将响应体的信息转化为字符串
            res = json.loads(html)#把类json的格式转化为字典
            #如果是第一页，就获取页码信息
            if pn==1:
                pagesize = res['content']['pageSize']
                totalcount=res['content']['positionResult']['totalCount']
                page = math.ceil(totalcount/pagesize)
            #获取招聘信息，并保存到MongoDB
            result = res['content']['positionResult']['result']
            for i in range(len(result)):
                save_mongodb(result[i])
            return res
        else:
            print('出现错误',html.status)
            return None
    except URLError:
        print('出现异常！')
        return None

#保存到MongoDB
def save_mongodb(info):
    if db[MONGO_TABLE].insert(info):
        print('保存成功！',info)
    else:
        print(info,'保存失败！',info)

#主体函数
def main():
    get_postion_info()#获取第一页的信息和页码信息
    #爬取第二页以后的信息
    for p in range(2,page+1):
        get_postion_info(pn=p)

if __name__=='__main__':
    main()
