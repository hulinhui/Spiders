# 驾驶员考试网(https://www.jsyks.com/kmy-mnks)


import time

import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()


def get_result(answer_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
        "Referer": "https://www.jsyks.com/hn"}
    Analysis_page_url = f'https://tiba.jsyks.com/Post/{answer_id}.htm'
    text = requests.get(Analysis_page_url, headers)
    seletor = etree.HTML(text.text)
    answer_text = seletor.xpath('//div[@id="question"]/h1/u/text()')[0]
    if answer_text == '对':
        answer_result = '正'
    elif answer_text == '错':
        answer_result = '错'
    else:
        answer_result = answer_text

    return answer_result


driver.get('https://www.jsyks.com/kmy-mnks')

li_list = driver.find_elements_by_css_selector('ul.Content > li')
for li in li_list:
    serial_No = li.find_element_by_css_selector('i').text
    question = li.find_element_by_css_selector('strong').text
    answer_id = li.get_attribute('c')
    print(f'问题{serial_No}、{question}')
    answer_result = get_result(answer_id)
    print(f"当前问题的答案是:{answer_result}")
    b_list = [i.text[0] for i in li.find_elements_by_css_selector('b')]
    for b_index, b_text in enumerate(b_list, 1):
        if b_text == answer_result:
            li.find_element_by_xpath(f'//b[{b_index}]').click()
            print(f'当前问题选中的答案是:{answer_result}')
        else:
            pass
    driver.execute_script('window.scrollBy(0,250)')
    time.sleep(2)
