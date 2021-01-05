import asyncio

from pyppeteer import launch



async def main():
    browser = await launch(headless=False, userDataDir='./userdata',
                           args=['--disable-infobars', '--no-sandbox', '--window-size=1366,850'], dumpio=True)
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await page.goto('https://www.baidu.com')
    await page.type('input#kw','python')
    await page.click('input#su')
    await asyncio.sleep(1)
    pagenum=1
    while pagenum<3:
        print(f"正在打印搜索页第{pagenum}页数据")
        await page.evaluate("window.scrollBy(0,document.body.scrollHeight)")
        await asyncio.sleep(1)
        elements = await page.querySelectorAll('#content_left > div h3 > a')
        for a in elements:
            title = await (await a.getProperty("textContent")).jsonValue()
            print(title)
        await page.click('.page-inner > a:last-child')
        pagenum+=1
        await asyncio.sleep(1)
    await browser.close()



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
