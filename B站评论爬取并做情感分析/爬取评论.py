import jsonpath
import requests
import re
import jsonpath
import json
from snownlp import SnowNLP
import matplotlib.pyplot as plt

# url = "https://api.bilibili.com/x/v2/reply/main?callback=jQuery331021989269820743784_1669726569039&jsonp=jsonp&next=0&type=1&oid=731732045&mode=3&plat=1&_=1669726569040:formatted"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
#     'Referer': 'https://www.bilibili.com/video/BV1JD4y1r7Ns/?spm_id_from=333.1007.tianma.19-4-72.click&vd_source=9c7252343e7cbc2c4b0243e5b5c0680c'
#           }

# url = 'https://api.bilibili.com/x/v2/reply/main?callback=jQuery331002962661434318714_1669795580531&jsonp=jsonp&next=0&type=1&oid=432542944&mode=3&plat=1&_=1669795580532:formatted'
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.9231 SLBChan/30',
#     'referer':'https://www.bilibili.com/video/BV1pG411F7KT/?spm_id_from=333.1007.tianma.6-1-17.click&vd_source=9c7252343e7cbc2c4b0243e5b5c0680c'
# }


# 韩语高级语法课程评论
# url = 'https://api.bilibili.com/x/v2/reply/main?callback=jQuery33109489176137820425_1669799700807&jsonp=jsonp&next=0&type=1&oid=844666505&mode=3&plat=1&_=1669799700808:formatted'
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.9231 SLBChan/30',
#     'referer': 'https://www.bilibili.com/video/BV1p54y187Bj/?spm_id_from=333.999.0.0&vd_source=9c7252343e7cbc2c4b0243e5b5c0680c'
# }


# 韩语初级入门
url = 'https://api.bilibili.com/x/v2/reply/main?callback=jQuery33108972148250111085_1669800158728&jsonp=jsonp&next=0&type=1&oid=52118083&mode=3&plat=1&_=1669800158729:formatted'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.9231 SLBChan/30',
    'Referer': 'https://www.bilibili.com/video/BV1w4411e7Bz/?spm_id_from=333.999.0.0&vd_source=9c7252343e7cbc2c4b0243e5b5c0680c'
}

res = requests.get(url,headers=headers)
print(res.content.decode())

# 提取子评论
messages =re.findall(r'"message":"(.*?)",',res.content.decode())[1:]
for i in range(len(messages)):
    for k in messages:
        if k == '':
            messages.remove(k)
print(messages)
unames = re.findall(r'"uname":"(.*?)"',res.content.decode())
# print(unmes)
time = re.findall(r'"time_desc":"(.*?)"',res.content.decode())
# print(time)
#
# 保存到表格中
import xlwt
# 实例化表格
workbook = xlwt.Workbook(encoding='utf-8')

# 实例化一个sheet
worksheet=workbook.add_sheet('sheet_000001')
# 第一个值为行，第二个值为列，第三个值为内容
worksheet.write(0,0,'姓名')
worksheet.write(0,1,'评论')
worksheet.write(0,2,'情感得分')
worksheet.write(0,3,'分析结果')
# worksheet.write(0,4,'时间')

# NLP 自然语言处理
# SnowNLP
# SnowNLP('内容').sentiments
# 分数在0-1之间，我们可以定义为小于0.5的为消极情绪，大于0.5的为积极情绪

# 统计情绪
pos_count = 0 #积极情绪计数器
neg_count = 0 #积极情绪计数器
print(len(messages))
print(len(unames))
print(len(time))
print(messages[len(messages)-1])
# print(messages)
# print(messages[56])
for i in range(len(messages)):
    name = unames[i]
    mes =  messages[i]
    # time = time[i]
    sentiments_score = SnowNLP(mes).sentiments
    if sentiments_score<0.5:
        tag = '消极'
        neg_count+=1
    else:
        tag = '积极'
        pos_count+=1
    worksheet.write(i+1, 0, name)
    worksheet.write(i+1, 1, mes)
    worksheet.write(i+1, 2, sentiments_score)
    worksheet.write(i+1, 3, tag)
    # worksheet.write(i+1, 4, time)
workbook.save('韩语零基础入门评论情感分析2.xls')

# 统计一些评论的情绪分别的占比
# 考虑分母为0
try:
    print('消极评论占比',round(neg_count/(neg_count+pos_count),4))
    print('积极评论占比',round(pos_count/(neg_count+pos_count),4))
except Exception as e:
    print('程序出现异常',e)


