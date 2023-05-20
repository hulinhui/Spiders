import requests
import re


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
        'Cookie': 'V2EX_LANG=zhcn; PB3_SESSION="2|1:0|10:1684392018|11:PB3_SESSION|44'
                  ':djJleDoyNDA3OmQ4NDA6NDA6OjEzNTo3NTczNDU4NA'
                  '==|05bcf42a4766de5cc22e46d4e68a7b7527427c337060aa9088bca689462dd422"; '
                  'V2EX_REFERRER="2|1:0|10:1684392024|13:V2EX_REFERRER|12:Q29sb1Rob3I'
                  '=|9f0ea6a0d30b251d2ec71670e01b9806f804f28c3c551cd3fbf9cc362164cee4"; '
                  'A2="2|1:0|10:1684481080|2:A2|48:YzY0ODYxMDQtMzk3ZC00Yzc4LTgzZWMtYTQ4ODdlNTdjMTgw'
                  '|ecc6003751e946c1a7d95d0eca7ab7c25c6d1380a64a00620b75cc194aa14834"; '
                  'V2EX_TAB="2|1:0|10:1684481087|8:V2EX_TAB|8:dGVjaA'
                  '==|4b990b6d35098ed174b82709271afe354870febcca0689a7e22ab4b767d2929f"; '
                  'V2EXSETTINGS="2|1:0|10:1684481087|12:V2EXSETTINGS|16:eyJuaWdodCI6IDB9'
                  '|5d09eda2ad671db12c2aad00765fa3cfeff7c23b4f7b58e84181e485e694e9df" '
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response
    except Exception as e:
        print(e)


def get_sign_result(html):
    if not html:
        print('签到失败！')
    message_text = re.search('<span.*?gray"><li.*?/li>.*?;(.*?)</span>', html.text, re.S).group(1)
    sign_day_text = re.findall('<div class="cell">(.*?)</div>', html.text, re.S)[-1]
    sign_text = f'{message_text},{sign_day_text}'
    return sign_text


def get_sign_href(text):
    v2ex_domain = 'https://www.v2ex.com'
    if not text:
        print('签到页面访问失败！')
        return
    link_data = re.search('<input type="button.*?location.href = \'(.*?)\';" />', text.text, re.S)
    if not link_data:
        print('未匹配到签到url！')
        return
    return v2ex_domain + link_data.group(1)


def main():
    page_url = 'https://www.v2ex.com/mission/daily'
    html1 = get_html(page_url)
    # print(html1.text)
    sign_url = get_sign_href(html1)
    print(sign_url)
    html3 = get_html(sign_url)
    print(html3.text)
    html2 = get_html(page_url)
    message = get_sign_result(html2)
    print(message)


if __name__ == '__main__':
    main()
