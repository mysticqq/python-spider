import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

#处理薪酬数据
#薪酬为区间分布的字符串
#找到20%的点作为薪酬
def deal_salary(salaries):
    salary=salaries.replace('k','').replace('K','').split('-')
    sal = int(salary[0]) + int((int(salary[1])-int(salary[0]))*0.2)
    return sal

#薪酬分布
def salary_distribution(series):
    plt.figure(figsize=(10,8))#图形大小
    series.plot.hist(bins=20,density=True)#条形图
    plt.title('数据分析师薪酬分布',fontsize=20)
    plt.xlabel('K/月',fontsize=15)
    plt.ylabel('频率',fontsize=15)
    plt.savefig('image/SalaryDistribution.png',dpi=400)#保存图片

#主要城市的薪酬分布
#每个城市对应的招聘信息数量不一样
#需要将每个城市的薪酬提取出来，作为一个元素存到city_salary列表中，便于绘制箱型图
def salary_city_distribution(df):
    main_city = ['北京','上海','深圳','广州','杭州']#主要城市
    df = df[df['city'].isin(main_city)]#提取包含主要城市的数据
    city_salary=[]
    #提取不同城市的数据列表，
    for city in main_city:
        money_li=list(df[df['city']==city]['money'])
        city_salary.append(money_li)
    plt.figure(figsize=(10,8))
    plt.boxplot(city_salary)#绘制箱型图
    plt.title('不同城市的薪酬分布',fontsize=20)
    plt.xticks(range(1,len(main_city)+1),main_city,fontsize=12)#修改刻度信息
    plt.ylabel('K/月',fontsize=15)
    plt.savefig('image/SalaryCityDistribution.png',dpi=400)#保存

#不同教育背景下的薪酬情况
def salary_education_distribution(df):
    #基于‘education’进行分组，合并‘money’的中位数，并进行排序
    edu_salary=df.groupby('education')['money'].median().sort_values()
    plt.figure(figsize=(10,8))
    edu_salary.plot(kind='bar')#绘制柱状图
    x=range(len(edu_salary))
    y=list(edu_salary)
    #添加薪酬的数字标签
    for a,b in zip(x,y):
        plt.text(a-0.01,b+0.2,str(b),verticalalignment='center',fontsize=12)
    plt.title('不同教育背景的薪酬分布',fontsize=20)
    plt.xlabel('')
    plt.ylabel('K/月',fontsize=15)
    plt.xticks(x,list(edu_salary.index),rotation=0)#修改刻度信息
    plt.savefig('image/EducationSalaryDistribution.png',dpi=400)#保存
    # plt.show()

#不同工作年限对薪酬的影响
def salary_workyear_distribution(df):
    df=df[df['workYear']!='10年以上']#因为‘10年以上’数量比较少，直接剔除
    # 基于‘workYear’进行分组，合并‘money’的平均数，并进行排序，四舍五入保留整数
    workyear_sal=df.groupby('workYear')['money'].mean().sort_values().round(0)
    x = range(len(workyear_sal))
    y = list(workyear_sal)
    workyear_sal.plot(kind='bar')#绘制柱状图
    #添加每个柱状对应的薪酬标签
    for a,b in zip(x,y):
        plt.text(a-0.1,b+0.5,str(b),verticalalignment='center',fontsize=12)
    plt.xticks(x,list(workyear_sal.index),fontsize=12,rotation=0)
    plt.ylabel('K/月',fontsize=15)
    plt.title('不同工作经验的薪酬分布')
    plt.savefig('image/WorkYearSalaryDistribution.png', dpi=400)#进行保存

if __name__=='__main__':
    data = pd.read_csv('data/LagouPostion.csv',encoding='gb18030')#打开文件
    data = data[data['jobNature']=='全职']
    data['money']=data['salary'].apply(deal_salary)#处理薪酬salary的数据
    salary_distribution(data['money'])#薪酬分布
    salary_city_distribution(data[['money','city']])#不同城市的薪酬分布
    salary_education_distribution(data[['education', 'money']])#不同教育背景下的薪酬情况
    salary_workyear_distribution(data[['workYear', 'money']])#工作年限对薪酬的影响
