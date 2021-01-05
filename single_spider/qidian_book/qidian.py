import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
from fontTools.ttLib import TTFont
from io import BytesIO


headers={'User-Agent':UserAgent().random}


def get_detail_href(page):
    all_book_format='https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page={}'
    print(f'正在爬取页面{page}')
    response=requests.get(all_book_format.format(page),headers=headers)
    if response.status_code==200:
        soup=BeautifulSoup(response.text,'lxml')
        li_list=soup.select('div.book-img-text > ul > li')
        for li in li_list:
            detail_url='https:'+li.select('div.book-mid-info > h4 > a')[0].get('href')
            font_info=get_detail_html(detail_url)
            font_dic = get_font(font_info[0])
            real_dic={str(k):str(parse_dic()[key]) for k in font_dic for key in parse_dic() if key==font_dic[k]}
            data_list=get_text(real_dic,font_info[1])
            print('字数：',data_list[0])
            print('会员推荐：', data_list[1])
            print('总推荐：', data_list[2])
            print('周推荐：', data_list[3])
    else:
        print(f'页面{page}访问失败，状态码为{response.status_code}')

def get_detail_html(url):
    print(f'正在爬取详情页:{url}')
    resp=requests.get(url,headers=headers)
    if resp.status_code==200:
        url_pattern=re.compile(", url\('(.*?)'\) format\('truetype'\)")
        text_pattern=re.compile("</style><span.*?>(.*?)</span></em><cite>(.*?)</cite>")
        ttf_url=url_pattern.search(resp.text,re.S).group(1)
        replace_text=text_pattern.findall(resp.text,re.S)
        return ttf_url,replace_text
    else:
        print(f'爬取失败详情页:{url}')

def get_font(url):
    resp=requests.get(url)
    font=TTFont(BytesIO(resp.content)) #BytesIO() 返回文件操作符【f】
    font_dic=font.getBestCmap()
    return font_dic

def get_text(item,textlist):
    data_text=[]
    for text in textlist:
        new_html = None
        for key in item:
            if new_html is None:
                new_html=text[0].replace(key,item[key])
            else:
                new_html=new_html.replace(key,item[key])
        data_text.append(new_html.replace('&#','').replace(';','')+text[1])
    return data_text


def parse_dic():
    python_font_relation ={
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'zero': 0,
        'period': '.'
    }
    return python_font_relation

def main():
    for page in range(1,3):
        get_detail_href(page)




if __name__ == '__main__':
    main()