"""
爬取全国各大城市的必胜客餐厅
@Author Andchann
@Data 2018-11-8
"""

import time
import json
import requests
from urllib.parse import quote
from lxml import etree

# 全国有必胜客餐厅的城市，我将城市放到文件中，一共380个城市
cities = []


def get_cities():
    """从文件中获取城市"""
    file_name = 'cities.txt'
    with open(file_name, 'r', encoding='UTF-8')as file:
        for line in file:
            city = line.replace('\n', '')
            cities.append(city)

    count = 1
    results = {}
    # 依次遍历所有城市的餐厅
    for city in cities:
        restaurants = get_stores(city, count)
        results[city] = restaurants
        count += 1
        time.sleep(2)

    with open('results.json', 'w', encoding='UTF-8')as file:
        # indent 缩进
        file.write(json.dumps(results, indent=4, ensure_ascii=False))


def get_stores(city, count):
    """根据城市获取餐厅信息"""
    session = requests.Session()
    # 对[城市0|0]进行Url编码
    city_urlencode = quote(city + '|0|0')
    # 用来存储首页的cookies
    cookies = requests.cookies.RequestsCookieJar()

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                      'UBrowser/6.2.3964.2 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Host': 'www.pizzahut.com.cn',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }

    print('===========第', count, '个城市:', city, '============')
    resp_from_index = session.get('http://www.pizzahut.com.cn/', headers=headers)
    # 然后将原来cookies的iplocation字段，设置自己想要抓取城市
    cookies.set('AlteonP', resp_from_index.cookies['AlteonP'], domain='www.pizzahut.com.cn')
    cookies.set('iplocation', city_urlencode, domain='www.pizzahut.com.cn')

    page = 1
    restaurants = []
    while True:
        data = {
            'pageIndex': page,
            'pageSize': "50",
        }

        response = session.post('http://www.pizzahut.com.cn/StoreList/Index', headers=headers, data=data, cookies=cookies)
        html = etree.HTML(response.text)
        # 获取餐厅列表所在的div标签
        divs = html.xpath("//div[@class='re_RNew']")
        temp_items = []
        for div in divs:
            item = {}
            content = div.xpath('./@onclick')[0]
            # 过滤掉括号和后面的内容
            content = content.split('(\'')[1].split(')')[0].split('\',\'')[0]

            if len(content.split('|')) == 4:
                item['coordinate'] = content.split('|')[0]
                item['restaurant_name'] = content.split('|')[1] + '餐厅'
                item['address'] = content.split('|')[2]
                item['phone'] = content.split('|')[3]
            else:
                item['restaurant_name'] = content.split('|')[0] + '餐厅'
                item['address'] = content.split('|')[1]
                item['phone'] = content.split('|')[2]
            print(item)
            temp_items.append(item)

        if not temp_items:
            break
        restaurants += temp_items
        page += 1
        time.sleep(5)
    return restaurants


if __name__ == '__main__':
    get_cities()
