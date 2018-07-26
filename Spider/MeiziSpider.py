import requests
from bs4 import BeautifulSoup
import os

#请求获得响应体
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    return html

#解析得到首页下每个图片下对应的网站链接
def get_page_url(url):
    html=get_html(url).text
    page_urls=[]
    soup = BeautifulSoup(html,'lxml')
    results=soup.select('#picture > p > a')#用css选择器进行解析
    for result in results:
        page_urls.append(result.attrs['href'])
    return page_urls

#获得每个图片的url
def get_img_url(page_urls):
    img_urls=[]
    for url in page_urls:
        html=get_html(url).text
        soup = BeautifulSoup(html, 'lxml')
        rs = soup.select('#picture > p > img')#进行解析获得图片url所在节点
        for r in rs:
            img_urls.append(r.attrs['src'])
    return img_urls

#完成请求，获得图片的二进制码，并进行保存
def save_img(img_urls):
    for url in img_urls:
        img=get_html(url).content#获得图片的二进制流
        file=url.split('uploads/')
        name=file[-1].replace('/','_')#每个图片的名字
        with open(name,'wb') as f:
            f.write(img)#进行保存

#主体函数
def main(folder='xxoo'):
#    os.mkdir(folder)#创建一个文件夹
#    os.chdir(folder)#切换到当前
    url='http://www.meizitu.com/'
    page_urls=get_page_url(url)#获得图片对应的网站链接
    img_urls=get_img_url(page_urls)#获得图片的链接
    save_img(img_urls)#保存图片


if __name__=='__main__':
    main()