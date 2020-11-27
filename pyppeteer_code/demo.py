import asyncio

from pyppeteer import launch


async def main():
    browser = await launch(headless=False, userDataDir='./userdata',
                           args=['--disable-infobars', '--no-sandbox', '--window-size=1366,850'], dumpio=True)
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await page.goto('https://s.taobao.com/search?q=手机')
    html = await page.content()
    print(html)
    await asyncio.sleep(100)
    await browser.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
