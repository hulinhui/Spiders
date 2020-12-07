# -*- coding: utf-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         maoyan_movies
# Description:  
# Author:       hlh
# Date:      2020/12/7 22:10
#-------------------------------------------------------------------------------
#第一步：找到字体文件，下载下来。
#第二步：通过Font Creator工具读取下载好的字体文件。
#第三步：按顺序拿到各个字符的unicode编码，并写出对应的文字列表。
#第四步：将顺序unicode编码写成对应的unicode的类型。
#第五步：替换掉文章中对应的unicode的类型的文字。
#--------------------------------------------------------------------------------
import requests
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
from io import BytesIO


headers={'User-Agent':UserAgent(verify_ssl=False).random}
HOST='https://maoyan.com'
fontdict = {'uniF489': '0', 'uniE137': '8', 'uniE7A1': '9', 'uniF19B': '2', 'uniF4EF': '6',
            'uniF848': '3', 'uniE343': '1', 'uniF53E': '4', 'uniE5E2': '5', 'uniF88A': '7',}



def get_moviescore(url):
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        soup=BeautifulSoup(response.text,'lxml')
        ddlist=soup.select('dl.movie-list > dd')
        for dd in ddlist:
            a=dd.select_one('a')
            if a is not None:
                detail_url=HOST+a.get('href')
                get_detail_html(detail_url)
            else:
                print('qqq')
    else:
        print(f'页面获取失败{url},状态码为:{response.status_code}')

def get_detail_html(url):
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        detail_text=response.text
        movies={}
        soup=BeautifulSoup(detail_text,'lxml')

        #电影名称
        movies['name']=soup.select_one('div.movie-brief-container > h1').string
        #电影英文名称
        movies['enname']=soup.select_one('div.movie-brief-container > div ').string
        #电影标签
        movies_tag=soup.select('div.movie-brief-container > ul > li:nth-of-type(1)> a')
        movies['movies_tag']=[tag.text.strip() for tag in movies_tag]
        #电影国家
        movies_country=soup.select('div.movie-brief-container > ul > li:nth-of-type(2)')[0].text
        movies['movies_country']=movies_country.split('/')[0].strip()
        #电影时长
        movies['movies_time'] = movies_country.split('/')[-1].strip()
        #上映时间
        movies['datetime']=soup.select('div.movie-brief-container > ul > li:nth-of-type(3)')[0].text
        #获取字体文件解析[不使用，规律见fontdict]
        # font_pattern=re.compile(",[\w\W]+?url\('(.*?)'\) format\('woff'\);")
        # font_url='http:'+font_pattern.search(detail_text,re.S).group(1)
        # font_dic=get_font(font_url)
        #猫眼口碑
        data_info=re.findall('<span class="stonefont">(.*?)</span>',detail_text,re.S)
        datalist=[]
        for data in data_info:
            data=data.replace('&#x','').replace(';','')
            new_html = None
            for key in fontdict:
                if new_html is None:
                    new_html = data.replace(key[3:].lower(),fontdict[key])
                else:
                    new_html = new_html.replace(key[3:].lower(),fontdict[key])
            datalist.append(new_html)
        print(datalist)
    else:
        print(f'详情页获取失败{url},状态码为:{response.status_code}')


def get_font(url):
    resp=requests.get(url,headers=headers)
    font=TTFont(BytesIO(resp.content))
    font_dic=font.getBestCmap()
    return font_dic



def main():
    url='https://maoyan.com/films'
    get_moviescore(url)





if __name__=='__main__':
    main()