# -*- coding: utf-8 -*-
import scrapy
import re
import json
from Bra.items import JdbraItem

# 分析网页的主要思路
# （1）我们主要是为了获取商品的销售数据（评论数据），首先找到商品的销售数据，跟网页呈现的相同
# （2）找到对应的链接，分析链接里面包含的主要信息：有商品的ID——ProductId、评论数据的页码——page
# （3）接下来主要考虑不同的商品对应的ID，看网站的URL会发现有ProductID的信息，就可以以此确定通过京东搜索页面，
#     输入关键字，我们可以基于呈现的页面来分析，可以获取商品的ProductID

# 爬虫的主要思路：
# （1）通过搜索商品关键字，来得到关于商品的页面，点击“销量”进行排序，基于该页面的URL完成，发送请求，获取商品ProductID
# （2）得到商品ProductID之后，构建评论数据对应的链接，进行请求，获得该商品的评论数据最大页码maxpage
# （3）得到最大页码之后，可以重新基于商品ProductId和页数page，重新构建评论数据的URL，进行请求，获得每个商品，每页下面的销售数据
# （4）获得响应进行解析，提取感兴趣的数据，并进行保存。

class JdbraSpider(scrapy.Spider):
    name = 'jdbra'
    #allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']
    #对应的搜索商品的URL
    url = 'https://search.jd.com/Search?keyword=%E8%83%B8%E7%BD%A9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&click=0'

    #初始请求
    def start_requests(self):
        yield scrapy.Request(url=self.url,callback=self.parse_product)

    #解析商品页面的信息
    def parse_product(self, response):
        productid=response.css('.gl-item::attr(data-sku)').extract()#获得ProductId
        productid = list(set(productid))#去重
        #请求，主要是为了获得每个商品的评论页码数量
        for product in productid:
            url_comment = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv7&productId='+product+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url_comment,callback=self.parse_page)

    #解析，获得每个ProductId对应的商品评论页数，基于页码数量和ProductId进行请求
    def parse_page(self,response):
        productid = re.search(r'productId=(\d+)&',response.url).group(1)
        maxpage = int(re.search(r'"maxPage":(\d+),',response.text).group(1))
        for page in range(maxpage):
            url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv7&productId='+productid+'&score=0&sortType=5&page='+str(page)+'&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url,callback=self.parse_comment)

    #解析获得评论里面的主要信息
    def parse_comment(self, response):
        #剔除多余的信息，变成类json的样式
        html = response.text.replace('fetchJSON_comment98vv7(','')
        html = html.replace(');','')
        comment = json.loads(html)#载入，变成字典
        results = comment['comments']
        #提取评论信息，构建item，传入pipeline
        for i in range(len(results)):
            item  = JdbraItem()
            item['content'] =results[i]['content']
            item['creationTime']=results[i]['creationTime']
            item['id'] = results[i]['id']
            item['productColor'] = results[i]['productColor']
            item['productSize'] = results[i]['productSize']
            item['score'] = results[i]['score']
            item['userClientShow'] = results[i]['userClientShow']
            item['userLevelName'] = results[i]['userLevelName']
            yield item