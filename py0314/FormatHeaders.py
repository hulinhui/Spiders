# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         FormatHeaders
# Description:  
# Author:       hlh
# Date:      2023/5/21 9:51
# -------------------------------------------------------------------------------

from lxpy import copy_headers_dict

header_rl = """
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0
X-Requested-With: XMLHttpRequest
Cookie: ASP.NET_SessionId=zbgisv041bnxktotlx1dcn2t
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
"""

header_jl = """
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
Origin: https://www.juliangip.com
"""

header_af = """
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
Accept: application/json, text/plain, */*
"""

header_v2 = """
Host: www.v2ex.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61
Cookie: {}
"""

header_ql = """
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: no-cache
Host: {}
Pragma: no-cache
Proxy-Connection: keep-alive
Content-Type: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61
"""

headers_yy = """
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61
Content-Type: application/json
"""

headers_gw = """
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61
"""

headers_ikuuu = '''
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61
origin: https://ikuuu.art
'''

headers_xingkong = '''
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: no-cache
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Host: www.xkdaili.com
Origin: https://www.xkdaili.com
Pragma: no-cache
Proxy-Connection: keep-alive
Referer: https://www.xkdaili.com/aspx/home.aspx
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61
X-Requested-With: XMLHttpRequest
'''

headers_xiongmao = '''
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: no-cache
Host: www.xiongmaodaili.com
Origin: http://www.xiongmaodaili.com
Pragma: no-cache
Proxy-Connection: keep-alive
Referer: http://www.xiongmaodaili.com/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61
'''

headers_one = '''
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: no-cache
Connection: keep-alive
Content-Length: 0
Cookie: guid=98e03f642f3317ae73b838e6ee866e85; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; ps=needv%3D0; 51job=cuid%3D141222074%26%7C%26cusername%3DE%252BGiK0Zaz9XUQ07IDRe2AUJ9b3PsgQw%252FM7Q3CdJwMPw%253D%26%7C%26cpassword%3D%26%7C%26cname%3DVT1LGobou%252FctBF1khRnRnQ%253D%253D%26%7C%26cemail%3Dpb7hakB24RoZJnT7gb%252BkkO8RJAnThJHRav1nJGLal2k%253D%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0Ar6wJxITgyk%26%7C%26cconfirmkey%3D17nCu3lBLwdy6%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D17sWIbm42btJI%26%7C%26to%3Dba11e0adcd81d8888e2e0baa8b2d26f36472c032%26%7C%26; sensor=createDate%3D2018-06-09%26%7C%26identityType%3D1; partner=www_google_com_hk; seo_refer_info_2023=%7B%22referUrl%22%3A%22https%3A%5C%2F%5C%2Fwww.google.com.hk%5C%2F%22%2C%22referHost%22%3A%22www.google.com.hk%22%2C%22landUrl%22%3A%22%5C%2F%22%2C%22landHost%22%3A%22www.51job.com%22%2C%22partner%22%3Anull%7D; privacy=1685772358; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22141222074%22%2C%22first_id%22%3A%22188584c9c131ed-08bc15a1bf3eb8-4c657b58-1049088-188584c9c14927%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg4NTg0YzljMTMxZWQtMDhiYzE1YTFiZjNlYjgtNGM2NTdiNTgtMTA0OTA4OC0xODg1ODRjOWMxNDkyNyIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjE0MTIyMjA3NCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22141222074%22%7D%2C%22%24device_id%22%3A%22188584c9c131ed-08bc15a1bf3eb8-4c657b58-1049088-188584c9c14927%22%7D; slife=lastlogindate%3D20230603%26%7C%26securetime%3DBzsHMlE%252FBWRVMFZhWmNZNgQyBjU%253D; acw_sc__v2=647b54ffacb01cc483d6849500377cc9f0efede2; acw_tc=ac11000116858042942651658e00de6050af9173734ca26817dbcfc2686128; search=jobarea%7E%60%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60040000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60040000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60040000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60040000%A1%FB%A1%FA041000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; acw_sc__v3=647b59de5ddbc6d442bdd8c0b77d24e291f09f46; ssxmod_itna=eqRxnQi=GQ57uDBP3tCDCbHDQEmh7g4BIAI63D/W+DnqD=GFDK40EA7qtu6pm=bE/x7I3q1BYcYQLtInhXWkmFo4GLDmKDyKU7beDxaq0rD74irDDxD3DbbdDSDWKD9D0bSyuEXKGWDbo=Di4D+bkQDmqG0DDUH04G2D7Unl7w=bwijiWtYhkY457GnD0toxBLetPTKrac=0wiiPZXWKqGyUPGuATUln4bDCh=ZfMNTQYpPQY4Weo+e88Gdt7ww7zGPFBAEN4phbGG407mh0Ugf9DDAK7qol8YxD; ssxmod_itna2=eqRxnQi=GQ57uDBP3tCDCbHDQEmh7g4BIAI=G9iaDxBq7Ir5GaQ9I5Fzs58x8o2jke/pkIXxuUlM+ipVYBCEXIyKZkmWI8EzQormo64cMTsni897SE=OVw90+dtbV30RT5ml1Hsnv46mnMKszOK0QAtuAMIE4R0OUwUVijAPXT23xMisWQuPqlAG9M5=EuhslAKC9GGp83fLK0rd=3d7plExR33+KB0jUbeCDeIm9MEHAdfpQGIm1Fr8Y3IO4S35UrrqFAPP8+tXHYL6VFr5kOhB8ZMAUocxisH2mWZqXh9FfRzdnR6xc4xOosePGneOmGFCwkl++GXLZivANmemkA0V0N3btvCv10P+pUVltCnqqhKSGrqmp3xjsjD3peqlqzjY3/+4OvH4icBIqEv7fItOj0mvge3jWKtOWs0b1KE/nEDSoIRvE3auDo+z3M1IPxKW8KUtPvfI4ZTT2n0tP==cxbFcRngofnidWDG2F0KCx63gP8+P4yzVPRK0P+bG2hxzxDFqD+6hPz+p7BHYD===
Host: oauth.51job.com
Origin: https://we.51job.com
Pragma: no-cache
Referer: https://we.51job.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0
sec-ch-ua: "Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
'''

wechat_headers = '''
Host: mp.weixin.qq.com
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"
X-Requested-With: XMLHttpRequest
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41
sec-ch-ua-platform: "Windows"
Accept: */*
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&createType=0&token=1811859841&lang=zh_CN
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cookie:appmsglist_action_3008736571=card; RK=YHMEtt9NVS; ptcz=0a0f5be1a1425103643ebe867bc9dee3440bdb723806ed4bb16ae2bdbdb9687f; pgv_pvid=6228993056; ua_id=DP7FBGZAVQsGM5n1AAAAAKsyd3RfthWzYTiQZha2GiU=; wxuin=86305390662321; mm_lang=zh_CN; uuid=8595c8a41a776e8390a12c14690dbf85; rand_info=CAESINtPfkkxwWAJXVpBNpejrpm+SPUrWu6qk9f79/zMAhiB; slave_bizuin=3008736571; data_bizuin=3215104193; bizuin=3008736571; data_ticket=XF9c+zNbl4xJ1n4tgnjjEKtp2tqpbyQMih1M2i6bmt0E+brBtv09IPkPgGdxb0+4; slave_sid=SFRGWXVKcFBtcHZZQUVFaDdQTFNiMmcydGlNMGVJTVlsdGxEYXpWUU84YXM4VF9jYUVMbm0zSlhlVm4zZ2RmMG1LOV9hd3NYYUxzcUE0ZnhiSDNFSGlxc3dFQnFJTlRPTTlpd0RJQ28yNVVuVzlfRFRrWmVHcGx3YlgxZ09YTFRpQ25LWFRxZ3NVZEtCTG9O; slave_user=gh_8d7023ba706f; xid=c91900832fa6fd72efcc277384295cc1; _clck=3008736571|1|fcn|0; _clsk=16oi9c|1687341792064|2|1|mp.weixin.qq.com/weheat-agent/payload/record
'''

headers_ksd = '''
Host: yx.jsh.com
Connection: keep-alive
Content-Length: 113
Accept: application/json, text/plain, */*
Authorization: {}
MK-U-App-Code: gUsb9sx0eXEdMuc
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat
MK-Source-Code: casarte
Content-Type: application/json;charset=UTF-8
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate, br
Accept-Language: en-us,en
'''


def get_format_headers(text):
    format_headers = copy_headers_dict(text)
    return format_headers


def update_cookies(headers, value):
    item_cookies = {item.split('=', 1)[0]: item.split('=', 1)[1] for item in headers['Cookie'].split('; ')}
    item_cookies.update({'acw_sc__v2': value})
    new_cookies_text = '; '.join([f'{k}={v}' for k, v in item_cookies.items()])
    headers.update({'Cookie': new_cookies_text})


if __name__ == '__main__':
    headers_item = get_format_headers(headers_one)
    update_cookies(headers_item, '123456')
