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
        
        pattern = re.compile(r'<script>(.+)</script>')#先找到需要匹配的文本信息
        mes = pattern.findall(text)
        text = mes[0]
        
        text = ''.join(text.split())#去除空格方便匹配
        pattern = re.compile(r',"TrainName":"(.+?)}]}},')
        text = pattern.findall(text)
        
        print('车次     发车时间     到达时间       起点站名       终点站名                            座位类型(余票)(价钱)')
        for mes in text:#遍历查找每趟车
            pattern = re.compile(r'(.+)","Train')
            id = pattern.findall(mes)[0]
            print('{0:<11}'.format(id), end='')
            
            pattern = re.compile(r'"StartTime":"(.+)","End')#发车时间
            StartTime = pattern.findall(mes)[0]
            pattern = re.compile(r'"EndTime":"(.+)","Total')#到达时间
            EndTime = pattern.findall(mes)[0]
            print('{0}        {1}         '.format(StartTime, EndTime), end='')

            pattern = re.compile(r'"DepartureStationName":"(.+)","ArrivalStationID')#起点站名
            DepartureStationName = pattern.findall(mes)[0]
            pattern = re.compile(r'"ArrivalStationName":"(.+)","Departure')#终点站名
            ArrivalStationName = pattern.findall(mes)[0]
            print('{0:^5}\t     {1:^5}\t\t'.format(DepartureStationName, ArrivalStationName), end='')
            
            pattern = re.compile(r'"SeatTypeName":"(.+?)","Price"')#座位类型
            SeatTypeName = pattern.findall(mes)
            
            pattern = re.compile(r'"Price":(.+?),"Show')#价钱
            Price = pattern.findall(mes)

            pattern = re.compile(r'"Inventory":(\d+)')#余票
            Inventory = pattern.findall(mes)
            
            for i in range(len(SeatTypeName)):
                print(SeatTypeName[i] + '('+Inventory[i] + '张)(' + Price[i] + '￥)', end='\t')
            print()


url = init()
text = get(url)

find(text)

input('按Enter键退出！')