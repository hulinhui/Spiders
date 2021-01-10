import json
import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

headers = {'UserAgent': UserAgent().random, 'Referer': 'http://www.weather.com.cn/'}
detail_url = 'http://www.weather.com.cn/weather1d/{}.shtml'
js_url = 'http://d1.weather.com.cn/sk_2d/{}.html?'
city_url = 'https://j.i8tq.com/weather2020/search/city.js'
time_stamp = int(time.time() * 1000)


def get_html_data(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(e)


def create_item(text):
    new_item = {}
    old_item = json.loads(text.split('=')[1])
    for item_value1 in old_item.values():
        for item_value2 in item_value1.values():
            for value in item_value2.values():
                new_item[value['NAMECN']] = value['AREAID']
    return new_item


def get_city_id(city_names, item):
    ids_list = []
    for city_name in city_names:
        if city_name in item:
            ids_list.append(item[city_name])
        else:
            print(f'城市名称：{city_name}不存在！')
    return ids_list


def json_parse(data, item):
    try:
        json_data = json.loads(data.split('=')[1])
        item['城市'] = json_data['cityname']
        item['日期'] = json_data['date']
        item['天气'] = json_data['weather']
        item['温度'] = json_data['temp'] + '℃'
        item['风向'] = json_data['WD']
        item['风力等级'] = json_data['WS']
        item['相对湿度'] = json_data['SD']
        item['PM2.5'] = json_data['aqi_pm25']
        item['更新时间'] = json_data['time']
    except Exception as e:
        print(e)


def html_parse(data, item):
    soup = BeautifulSoup(data, 'lxml')
    li_selector = soup.select_one('div.livezs > ul ')
    # 穿衣指数
    item['穿衣指数'] = li_selector.select('li#chuanyi > a > p')[0].get_text()

    # 洗车指数
    item['洗车指数'] = li_selector.select_one('li:nth-of-type(5) > a > p').get_text()

    # 紫外线指数
    item['紫外线指数'] = li_selector.select_one('li:nth-of-type(6) > p').get_text()


def send_message(text):
    SCKEY = 'SCU113501Tecdb5f07d314e839004c0a02bc9f83b75f5d90f02600e'
    send_url = 'http://sc.ftqq.com/{}.send'
    data = {'text': f"{text['城市']}-{text['日期']}-天气播报：", 'desp': text}
    r = requests.post(send_url.format(SCKEY), data=data)
    if r.status_code == 200:
        if r.json()['errmsg'] == 'success':
            print('消息推送成功')
        else:
            print('消息发送失败')
    else:
        print(f'消息发送失败:{r.status_code}')


def get_city_html(city_ids):
    for city_id in city_ids:
        data_item = {}
        js_data = get_html_data(js_url.format(city_id))
        json_parse(js_data, data_item)
        html_data = get_html_data(detail_url.format(city_id))
        html_parse(html_data, data_item)
        send_message(data_item)


def main():
    text = get_html_data(city_url)
    new_item = create_item(text)
    city_names = input("请输入城市名称,多个城市查询请使用英文逗号分开：").strip().split(',')
    city_ids = get_city_id(city_names, new_item)
    get_city_html(city_ids)


if __name__ == '__main__':
    main()
