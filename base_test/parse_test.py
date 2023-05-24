# python爬虫网页解析之parse模块
from parsel import Selector
import requests


def get_html(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        selector = Selector(r.text)
        return selector
    except:
        print("产生异常")


def xpath_parse(selector):
    xpath_mode = '//title/text()'
    title = selector.xpath(xpath_mode).extract_first()
    print(title)


def css_parse(selector):
    css_path = 'title::text'
    title = selector.css(css_path).extract()[0]
    print(title)


def re_parse(selector):
    re_mode = '<title>(.*?)</title>'
    title = selector.re(re_mode)[0]
    print(title)


def main(url):
    selector = get_html(url)
    xpath_parse(selector)
    css_parse(selector)
    re_parse(selector)


if __name__ == '__main__':
    main(url='https://news.baidu.com/')
