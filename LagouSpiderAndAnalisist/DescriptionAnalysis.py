import pandas as pd
import numpy as np
import jieba
import matplotlib.pyplot as plt
from SalaryDistribution import deal_salary
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator

#获取常用的停用词
def get_stop_word(filepath='data/中文停用词库.txt'):
    word_list = []
    for line in open(filepath,'r'):
        word_list.append(line.strip())
    return word_list

#处理职位描述的信息
def deal_description(description):
    #剔除不用的信息
    description=description.replace('：','').replace('职位描述','').replace('岗位职责','').replace('岗位要求','').strip()
    #进行结巴分词
    seg_list = jieba.cut(description)
    word_list='/'.join(seg_list).split('/')
    #剔除词的list
    li = ['数据','分析','经验','数据分析','工作','能力','相关','熟悉','熟练','.','']
    #常见停用词列表
    stop_word =get_stop_word()
    word_li=[]
    #对获得词语进行处理
    for word in word_list:
        word=word.strip().upper()
        if 'EXC' in word:
            word = 'EXCEL'
        elif 'POWER' in word:
            word = 'PPT'
        elif '统计' in word:
            word = '统计学'
        elif '机器' in word:
            word = '机器学习'
        #如果词语不在停用词列表，
        # 和暂时还不在词的列表里面，
        # 不为空
        #不在剔除词的列表里面
        #就将该词加到词语列表里面
        if word not in stop_word and word not in word_li and word !=''and word not in li:
            word_li.append(word)
    return word_li

#统计词频
def get_word_dict(series):
    word_dict={}
    for word_list in list(series):
        for word in word_list:
            #如果在字典里面就+1
            if word in word_dict:
                word_dict[word] += 1
            #如果不在字典里面，就初始化为1
            else:
                word_dict[word] = 1
    # df = pd.Series(word_dict)
    # df.to_csv('data/cipin.csv',encoding='gb18030')
    return word_dict

#根据词频，进行词云统计
def word_cloud_description(word_dict):
    #背景图片，用来限制显示的形状
    backgroud = plt.imread('data/bra.jpg')
    #实例化词云对象
    wc = WordCloud(
        background_color='white',#背景颜色
        mask=backgroud,#背景图片
        font_path='C:\Windows\Fonts\msyh.ttf',#如果为中文，需要添加该路径
        max_words=1000,#设置最大实现的次数
        stopwords=STOPWORDS,#停用词
        max_font_size=100,#最大字体大小
        random_state=30#设置有多少种随机生成状态，即有多少种配色方案
    )
    wc.generate_from_frequencies(word_dict)#传入词频
    img_colors=ImageColorGenerator(backgroud)
    # wc.recolor(color_func=img_colors)
    plt.figure(figsize=(10, 8))
    plt.imshow(wc)#显示词云图
    plt.axis('off')#取出坐标轴
    plt.savefig('image/Description.png',dpi=400,bbox_inches='tight')#保存

#统计掌握主要技能对应的薪酬
def skill_salary(df):
    #主要技能
    main_skill=['EXCEL','PPT','PYTHON','R','统计学','HIVE','SPARK','机器学习']
    skill_salary = {}#用来记录对应技能的薪酬总和
    skill_count = {}#用来记录对应技能的数量
    for skill in main_skill:
        for i in range(len(df)):
            #判断该技能是否在对应的描述中，如果在，就执行下面的程序
            if skill in df['word'].iloc[i]:
                #如果该技能已经在对应字典的键中，就计算加和和数量
                if skill in skill_salary:
                    skill_salary[skill] += df['money'].iloc[i]
                    skill_count[skill] += 1
                #如果该技能还没出现在对应的字典里面，就进行初始化
                else:
                    skill_salary[skill] = df['money'].iloc[i]
                    skill_count[skill] = 1
    money={}
    #计算每个技能对应的平均薪酬
    for skill in skill_count:
        money[skill]=round(skill_salary[skill]/skill_count[skill],0)
    #可视化
    salary_s = pd.Series(money)#将字典转化为Series对象，便于图形显示
    plt.figure(figsize=(10,8))
    salary_s.plot(kind='bar')#柱状图
    x = range(len(salary_s))
    y = list(salary_s)
    #添加薪酬标签
    for a,b in zip(x,y):
        plt.text(a,b+0.2,str(b),horizontalalignment='center',fontsize=12)
    plt.xticks(x,list(salary_s.index),rotation=0)
    plt.ylabel('K/月',fontsize=15)
    plt.xlabel('')
    plt.title('主要技能的薪酬分布',fontsize=20)
    plt.savefig('image/MainSkillSalary.png',dpi=400)#保存

if __name__=='__main__':
    data = pd.read_csv('data/LagouPosition1234.csv',encoding='gb18030')#加载数据
    data['money'] = data['salary'].apply(deal_salary)#处理薪酬数据
    data['word'] = data['description'].apply(deal_description)#用jieba分词，提取文本信息转化为词语信息
    word_dict=get_word_dict(data['word'])#统计词频
    word_cloud_description(word_dict)#根据词频，绘制词云图
    skill_salary(data[['word','money']])#统计主要技能的薪酬