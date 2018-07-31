import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

#处理行业数据
#含有多个标签的只考虑第一个标签
def deal_industry(industries):
    industries=str(industries).replace('、',',').strip().split(',')[0].strip().split(' ')[0].strip()
    return industries

#不同城市的需求分布
def Area_distribution(series):
    city_counts = series.value_counts()#计算每个城市的频数
    city_c = city_counts[city_counts>=80]#取出需求数量大于等于80的城市和数量
    other_c = city_counts[city_counts<80].sum()#对小于80的进行求和
    other_c = pd.Series(other_c,index=['其他'])#编程Series对象，便于合并
    city_c=city_c.append(other_c)
    city_rate = city_c.div(city_c.sum())#除法，计算概率
    #可视化
    plt.figure(figsize=(8,8))#设置图形大小
    data = list(city_rate*100)
    label = list(city_rate.index)
    plt.pie(data,labels=label,autopct='%.2f%%')#画饼状图
    plt.title('数据分析师城市需求分布',fontsize=20)#添加标题
    plt.savefig('image/AreaDistribution.png',dpi=300,bbox_inches='tight')#保存图片
    # plt.show()

#不同行业的需求分布
def Industry_distribution(series):
    indu_counts=series.value_counts()
    indu_count=indu_counts[indu_counts>=60]
    other_c = indu_counts[indu_counts<60].sum()
    other_count = pd.Series(other_c,index=['其他'])
    indu_count=indu_count.append(other_count)
    indu_rate = indu_count.div(indu_count.sum())
    #可视化
    plt.figure(figsize=(8, 8))
    data = list(indu_rate * 100)
    label = list(indu_rate.index)
    plt.pie(data, labels=label, autopct='%.2f%%')
    plt.title('数据分析师行业需求分布', fontsize=20)
    plt.savefig('image/IndustryDistribution.png', dpi=300, bbox_inches='tight')#保存图片
    # plt.show()

#工作经验的需求分布
def Workyear_distribution(seires):
    workyears=seires.value_counts()
    workyears=workyears[workyears>10]#剔除小于10的数据
    workyears_rate=workyears.div(workyears.sum())
    # 可视化
    plt.figure(figsize=(8, 8))
    data = list(workyears_rate * 100)
    label = list(workyears_rate.index)
    plt.pie(data, labels=label, autopct='%.2f%%')
    plt.title('数据分析师经验需求分布', fontsize=20)
    plt.savefig('image/WorkYearDistribution.png', dpi=300, bbox_inches='tight')#保存
    # plt.show()

if __name__=='__main__':
    data = pd.read_csv('cities_position_info.csv',encoding='gb18030')#加载数据
    data = data[data['jobNature']=='全职']#滤除不为全职的岗位信息
    Area_distribution(data['city'])#处理和显示数据分析师的城市需求分布
    data['industry'] = data['industryField'].apply(deal_industry)#处理行业数据
    Industry_distribution(data['industry'])#处理和显示不同行业的需求分布
    Workyear_distribution(data['workYear'])#处理和显示工作经验的需求分布