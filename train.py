import requests
import re

def init():#初始化url
    chu = input('请输入起始地：')
    mo = input('请输入目的地：')
    date = input('请输入出行时间（YYYY-MM-DD）：')
    url = 'https://trains.tieyou.com/pages/trainList?fromCn='
    url += chu
    url += '&toCn='
    url += mo
    url += '&fromDate='
    url += date
    return url


def get(url):#尝试访问网页
    try:
        r = requests.get(url)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('Wrong')


def find(text):#查找班次信息
    pattern = re.compile(r'<a style="color: #333;" data-v-9079722a>(.+)</a>')
    zongcheci = pattern.findall(text)
    if len(zongcheci) == 0:
        print('查询日没有车次！')
    else:
        print('总共有' + zongcheci[0] + '趟车')

        pattern = re.compile(r'<strong data-v-9079722a>(.+)</strong>')
        checi = pattern.findall(text)

        pattern = re.compile(r'\d\d:\d\d')
        reslust = pattern.findall(text)
        time = reslust[:int(zongcheci[0])*2]

        pattern = re.compile(r'<div data-v-9079722a><span data-v-9079722a>(.+)</span>')
        Type = pattern.findall(text)
        Type = ['硬  座' if i=='硬座' else i for i in Type]#转换格式，以便后续匹配
        Type = ['硬  卧' if i=='硬卧' else i for i in Type]
        Type = ['软  卧' if i=='软卧' else i for i in Type]
        Type = ['动  卧' if i=='动卧' else i for i in Type]
        
        pattern = re.compile(r'余<em data-v-9079722a>(.+)</em>张')
        num = pattern.findall(text)


        for i in range(int(zongcheci[0])):#格式化输出更为好看
            #print(num[i*3+2])
            print('车次{0:0>2}为：{1: <8}发车时间为：{2}    到达时间为：{3}    票数剩余：{4}:{5:>2}；{6}:{7:>2}；{8}:{9:>2}'.format(i+1, 
                    checi[i*2], time[i*2], time[i*2+1], Type[i*3], num[i*3], Type[i*3+1], num[i*3+1], Type[i*3+2], num[i*3+2]))

url = init()
text = get(url)
find(text)

input('按Enter键退出！')