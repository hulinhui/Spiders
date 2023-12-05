#参考：https://www.cnblogs.com/hhh188764/p/14082028.html

import base64
import json

import requests
from fake_useragent import UserAgent
from fontTools.ttLib import TTFont
from lxml import etree

headers={'User-Agent':UserAgent().random}




def get_font(url,pagenum):
    response=requests.get(url.format(pagenum),headers=headers)
    if response.status_code==200:
        base64_string=response.text.split('base64,')[1].split("'")[0].strip()
        bin_data=base64.decodebytes(base64_string.encode())
        with open('58font.ttf','wb') as f:
            f.write(bin_data)
        font=TTFont('58font.ttf')
        font.saveXML('58font.xml')
        return response.text
    else:
        print(f'页面{pagenum}访问字体数据失败')

def find_font():
    #已glyph开头的编码对应的数字
    glyph_dic={
        'glyph00001': '0',
        'glyph00002': '1',
        'glyph00003': '2',
        'glyph00004': '3',
        'glyph00005': '4',
        'glyph00006': '5',
        'glyph00007': '6',
        'glyph00008': '7',
        'glyph00009': '8',
        'glyph00010': '9'}
    #十个加密字体编码
    unicode_list=['0x9476', '0x958f', '0x993c', '0x9a4b', '0x9e3a', '0x9ea3', '0x9f64', '0x9f92', '0x9fa4', '0x9fa5']
    font_data=etree.parse('./58font.xml')
    code_dict={}
    for unicode in unicode_list:
        result=font_data.xpath("//cmap//map[@code='{}']/@name".format(unicode))[0]
        for key in glyph_dic:
            if key==result:
                code_dict[unicode]=glyph_dic.get(key)
    code_dict_str=json.dumps(code_dict).replace('0x','&#x').replace('":',';":')
    code_dict_obj=json.loads(code_dict_str)
    print('已成功找到编码所对应的数字！')
    return code_dict_obj


def replace_font(item,key,text):
    return text.replace(key,item[key])


def replace_html(item,text):
    new_html = None
    for key in item:
        if new_html is None:
            new_html = replace_font(item, key, text)
        else:
            new_html = replace_font(item, key, new_html)
    return new_html

def parse_html(html):
    tree=etree.HTML(html)
    li_list=tree.xpath("//ul[@class='house-list']/li[contains(@class,'apartments') or contains(@class,'house-cell')]")
    item_list=[]
    for li in li_list:
        item={}
        region_list = li.xpath('.//p[@class="infor"]/a/text()')
        distance_list = ''.join(li.xpath('.//p[@class="infor"]/text()')).strip()
        jjr_list = li.xpath('./div[@class="des"]/div[@class="jjr"]//span/text()')
        send_time = li.xpath('./div[@class="list-li-right"]/div[@class="send-time"]/text()')

        item['title']=li.xpath('./div[@class="des"]/h2/a/text()')[0].strip()
        # item['href'] = li.xpath('./div[@class="des"]/h2/a/@href')[0].strip()
        item['room_size'] = li.xpath('./div[@class="des"]/p[@class="room"]/text()')[0].strip().split()[0]
        item['room_area'] = li.xpath('./div[@class="des"]/p[@class="room"]/text()')[0].strip().split()[1]
        item['price']=li.xpath('./div[@class="list-li-right"]/div[@class="money"]')[0].xpath('string(.)').strip()
        item['send_time']=send_time[0].strip() if send_time else ''
        item['region']='-'.join(region_list) if len(region_list) else ''
        item['distance']=distance_list if distance_list else ''
        item['agent']='-'.join([i.strip() for i in jjr_list if jjr_list])
        item_list.append(item)
        print(item)
    print(len(item_list))

if __name__ == '__main__':
    pn=2
    url_format='https://sz.58.com/chuzu/pn{}/'
    old_html=get_font(url_format,pn)
    code_dict=find_font()
    new_html=replace_html(code_dict,old_html)
    parse_html(new_html)

