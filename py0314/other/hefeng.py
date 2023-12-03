import os
import pathlib
from configparser import ConfigParser

import requests

from py0314.NotifyMessage import send_telegram
from py0314.loggingmethod import get_logging

logger = get_logging()  # 日志模块


def read_config():
    item_infos = {}
    config = ConfigParser()
    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_name, '../config.ini')
    if not os.path.exists(file_path):
        pathlib.Path(file_path).touch()  # 创建文件
    config.read(file_path, encoding='utf-8')
    for sec in config.sections():
        item_infos[sec] = {}
        for key, value in config.items(sec):
            item_infos[sec][key] = value
    return item_infos


def config_data(config_items):
    filename_capital = os.path.splitext(os.path.basename(__file__))[0].upper()
    return config_items[filename_capital]


def get_data(url, params):
    try:
        with requests.session().get(url, params=params) as resp:
            resp.raise_for_status()
            resp.encoding = 'uff-8'
            return resp.json()
    except:
        return None


def get_locationid(cityname, key):
    city_search_url = 'https://geoapi.qweather.com/v2/city/lookup?'
    params = {'location': cityname, 'key': key}
    json_data = get_data(city_search_url, params)
    if 'code' in json_data and json_data.get('code') == '200':
        lon = float(json_data['location'][0]['lon'])
        lat = float(json_data['location'][0]['lat'])
        return f"{lon:.2f},{lat:.2f}"
    else:
        logger.info('获取城市id失败')


def search_city_weather(location_lon_lat, key):
    ge_dian_weather_url = 'https://devapi.qweather.com/v7/grid-weather/3d?'
    city_weather_url = 'https://devapi.qweather.com/v7/weather/3d?'
    params = {'location': location_lon_lat, 'key': key}
    json_data = get_data(ge_dian_weather_url, params)
    json_data_2 = get_data(city_weather_url, params)
    if json_data.get('code') == '200' and json_data_2.get('code') == '200':
        for daily_data, daily_data_2 in zip(json_data['daily'], json_data_2['daily']):
            result_data = {key: daily_data[key] for key in daily_data if
                           not (key.startswith('icon') or key.startswith('wind360'))}
            weather_msg = f"预报日期：{result_data['fxDate']}\n气温：{result_data['tempMin']}-{result_data['tempMax']}℃，当天总降水量：{result_data['precip']}mm，相对湿度:{result_data['humidity']}%，紫外线指数：{daily_data_2['uvIndex']}，能见度：{daily_data_2['vis']}km，云量：{daily_data_2['cloud']}%，大气压强：{result_data['pressure']}bar\n白天天气：{result_data['textDay']}，日出日落：{daily_data_2['sunrise']}-{daily_data_2['sunset']}，白天风向：{result_data['windDirDay']}，白天风力等级：{result_data['windScaleDay']}，白天风速：{result_data['windSpeedDay']}km/h\n晚间天气：{result_data['textNight']}，月升月落：{daily_data_2['moonrise']}-{daily_data_2['moonset']}，月相：{daily_data_2['moonPhase']}，晚间风向：{result_data['windDirNight']}，晚间风力等级：{result_data['windScaleNight']}，晚间风速：{result_data['windSpeedNight']}km/h"
            return weather_msg
    else:
        logger.info('获取格点天气或城市天气失败！')


def send_qmsg(message, group_code, qmsg_key):
    send_group_url = 'https://qmsg.zendee.cn/group/{}?'
    params = {'msg': message, 'group': group_code}
    send_response = requests.get(send_group_url.format(qmsg_key), params=params)
    send_msg = send_response.json()
    if send_msg['success']:
        logger.info("今日天气播报推送成功！")
    else:
        logger.info(f"Qmsg推送出现问题了！--{send_msg['reason']}")


def weather_index(location_lon_lat, key):
    weather_index_url = 'https://devapi.qweather.com/v7/indices/1d?'
    params = {'location': location_lon_lat, 'key': key, 'type': '0'}
    json_data = get_data(weather_index_url, params)
    if 'code' in json_data and json_data.get('code') == '200':
        data_list = [f"【{daily_data['name']}--{daily_data['category']}】：{daily_data['text']}" for daily_data in
                     json_data['daily']]
        return '\n'.join(data_list)
        # for daily_data in json_data['daily']:
        #     print(f"【{daily_data['name']}--{daily_data['category']}】：{daily_data['text']}")
    else:
        logger.info('获取天气指数预报失败！')

    # print(json.dumps(json_data,ensure_ascii=False,indent=4))


def main():
    config_items = read_config()
    item_data = config_data(config_items)
    location_lon_lat = get_locationid(item_data['city_name'], item_data['hefeng_key'])
    if item_data['hefeng_key'] and location_lon_lat:
        message = search_city_weather(location_lon_lat, item_data['hefeng_key'])  # 格点天气及城市天气查询
        data_message = weather_index(location_lon_lat, item_data['hefeng_key'])  # 天气指数预报
        message = message + '\n' + data_message
        logger.info(message)
        # send_qmsg(message, item_data['group_code'], item_data['qmsg_key'])
        send_telegram()

    else:
        logger.info('参数不全，无法查询')


if __name__ == '__main__':
    main()
