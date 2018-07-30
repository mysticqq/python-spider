/*
    selenium渲染库模拟浏览器爬取淘宝js渲染的网页信息
    url='https://www.taobao.com/'
*/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import re
import pymongo

MONGO_URL='localhost'
MONGO_DB='Taobao'
MONGO_TABLE = 'Food'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

KEYWORD = '美食'

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)#设置显性等待时间



#搜索关键字，并提取信息
def search_page():
    url='https://www.taobao.com/'
    browser.get(url)#输入网址
    try:
        #找到对应搜索框
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
        #找到搜索按钮
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.clear()
        #输入关键字
        input.send_keys(KEYWORD)
        button.click()#点击执行
        #判断搜索之后的页面是否已经加载好
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.form > span.btn.J_Submit')))
        #获得页码信息
        page=browser.find_element(By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total').text
        #进行信息提取
        get_information(browser.page_source)
        return page
    except TimeoutException:
        print('搜索出现异常！')
        return search_page()#出现超时异常之后，重新执行该函数

#翻页操作，并提取信息
def get_next_page(pn):
    try:
        #找到页码的输入框
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        #页码的确定按钮
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        #清空输入框
        input.clear()
        #传入页码信息
        input.send_keys(pn)
        button.click()#点击执行
        #判断翻页之后，是否已经加载好
        #通过翻页之后的页码数是否高亮
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'.item.active > span'), str(pn)))
        #提取信息
        get_information(browser.page_source)
    except TimeoutException:
        print('异常处理！')
        get_next_page(pn)#如有异常，重新执行翻页操作

#根据获得HTML超文本，进行信息提取，并保存到数据库
def get_information(html):
    soup = BeautifulSoup(html,'lxml')
    names = soup.select('.title .J_ClickStat')
    prices = soup.select('.price strong')
    counts = soup.select('.deal-cnt')
    shops = soup.select('.shop > a')
    locations=soup.select('.row .location')
    for i in range(len(names)):
        food = {
            'name':names[i].get_text().strip(),
            'price':prices[i].get_text(),
            'count':counts[i].get_text()[:-3],
            'shop':shops[i].get_text().strip(),
            'location':locations[i].get_text()
        }
        save_to_mongo(food)#保存到数据库

#保存到数据库的函数
def save_to_mongo(food):
    if db[MONGO_TABLE].insert(food):
        print('保存成功',food)
    else:
        print('保存失败',food)

#主体函数
def main():
    page=search_page()#请求并进行关键字搜索，获得对应的页码信息和商品信息
    pattern = re.compile('(\d+)',re.S)
    page = int(re.search(pattern, page).group())#通过正则表达式提取页码信息
    #翻页
    for pn in range(2,page+1):
        get_next_page(pn)#执行翻页操作，并进行信息提取
    browser.close()#关闭浏览器

if __name__=='__main__':
    main()
