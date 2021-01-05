import requests
from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio
import tkinter


def screen_size():
    tk=tkinter.Tk()
    width=tk.winfo_screenwidth()
    height=tk.winfo_height()
    tk.quit()
    return width,height




async def main(url):
    browser= await launch(args=['--no-sandbox'])
    page=await browser.newPage()
    width,height=screen_size()
    await page.setViewport({'width': width, 'height': height})
    await page.setJavaScriptEnabled(True)
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    print(f"正在访问页面：{url}")
    await page.goto(url)
    while not await page.querySelector('#J_goodsList'):
        pass
    await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
    await asyncio.sleep(3)
    li_list=await page.xpath('//div[@id="J_goodsList"]/ul/li')
    for li in li_list:
        item={}
        a=await li.xpath('.//div[@class="p-img"]/a')
        em=await li.xpath('./div/div[3]/a/em')
        item['title']=await (await em[0].getProperty('textContent')).jsonValue()
        item['detail_url']=await (await a[0].getProperty('href')).jsonValue()
        a_=await li.xpath('.//div[@class="p-commit"]/strong/a')
        item['p_commit']=await (await a_[0].getProperty('textContent')).jsonValue()
        i=await  li.xpath('.//div[@class="p-price"]/strong/i')
        item['p_price']=await (await i[0].getProperty('textContent')).jsonValue()
        print(item)
    await close_page(browser)


async def close_page(browser):
    for _page in await browser.pages():
        await _page.close()
    await browser.close()




if __name__ == '__main__':
    shop_name='手机'
    url_format='https://search.jd.com/Search?keyword={}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={}&cid2=653&cid3=655&page={}'
    url_list=[url_format.format(shop_name,shop_name,i) for i in range(1,6)]
    tasks=[main(url) for url in url_list]
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
