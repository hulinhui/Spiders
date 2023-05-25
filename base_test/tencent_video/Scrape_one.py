# -*- coding: utf-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         Scrape_one.py
# Description:  
# Author:       hlh
# Date:      2022/3/15 17:38
# desc:      网页利用CSS控制文字的偏移位置，或者通过一些特殊的方式隐藏关键信息，对数据爬取造成影响
#-------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_browser():
    options=webdriver.ChromeOptions()
    prefs={"profile.managed_default_content_settings.images": 2}
    options.add_argument("--handless")
    options.add_experimental_option("pref",prefs)
    options.add_argument("lang=zh_CN.utf-8")
    browser=webdriver.Chrome(options=options)
    wait=WebDriverWait(browser,10)
    return wait,browser


def get_html(url,browser,wait):
    browser.get(url)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'')))






def main():
    url='https://antispider3.scrape.center/page/1'
    wait,browser=get_browser()
    get_html(url,browser,wait)



if __name__=='__main__':
    main()