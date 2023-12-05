import time

import requests

# 浏览器头部
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; U; Android 9; zh-cn; MI 6 Build/9.0) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1"
}
# 账号、密码
username = '975081281@qq.com'
passwd = 'Rr123456'


class RenRen():
    def __init__(self, username, passwd, headers):
        self.username = username
        self.passwd = passwd
        self.headers = headers
        self.token_login = "http://a.zmzapi.com/index.php?g=api/public&m=v2&accesskey=519f9cab85c8059d17544947k361a827&client=2&a=login&account={}&password={}"
        self.huodong_url = 'http://h5.rrhuodong.com/index.php?g=api/mission&m=index&a=login&uid={}&token={}'
        self.qiandao_login_url = 'http://h5.rrhuodong.com/index.php?g=api/mission&m=clock&a=store&id=2'
        self.userinfo_url = 'http://h5.rrhuodong.com/index.php?g=api/mission&m=index&a=user_info'

    def run(self):
        info = self.get_token()
        if info:
            cookies = self.get_cookies(info)
            self.qiaodao(cookies)
        else:
            print('获取登录信息失败')

    def get(self, url, cookies=None):
        content = requests.get(url, headers=self.headers, cookies=cookies, verify=False, allow_redirects=False)
        try:
            content.raise_for_status()
            content.encoding = content.apparent_encoding
        except Exception as e:
            print(e)
        return content

    def get_cookies(self, info):
        response = self.get(self.huodong_url.format(*info))
        if response.status_code == 200:
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            return cookies
        else:
            print(f'响应失败：{response.status_code}')

    def qiaodao(self, cookies):
        if cookies:
            response = self.get(self.qiandao_login_url, cookies)
            if response.status_code == 200:
                data_text = response.json()
                if data_text['status'] == 1:
                    text = self.get_user_info(cookies)
                    self.send_message(text)
                else:
                    print(f'签到失败!:{data_text["info"]}')
                    self.send_message(f'签到失败!：{data_text["info"]}')
            else:
                print(f'签到失败，状态码:{response.status_code}')
                self.send_message(f'签到失败，状态码:{response.status_code}')
        else:
            print('cookies获取失败')

    def send_message(self, text):
        server_key = 'SCU113501Tecdb5f07d314e839004c0a02bc9f83b75f5d90f02600e'
        send_url = 'http://sc.ftqq.com/{}.send'
        base_url = send_url.format(server_key)
        params = {"text": text, "desp": text}
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            json_data = response.json()
            if json_data['errno'] == 0:
                print("消息推送成功")
            else:
                print("推送失败")
        else:
            print(f'调用发送消息接口报错：{response.status_code}')

    def get_user_info(self, cookies):
        response = self.get(self.userinfo_url, cookies=cookies)
        if response.status_code == 200:
            json_data = response.json()
            if json_data['status'] == 1:
                data = json_data['data']
                message_text = f"{time.strftime('%Y-%m-%d', time.localtime())}签到成功!\n称昵:{data['nickname']},等级:{data['group_name'] + data['main_group_name']},人人钻:{data['point']}"
                return message_text
            else:
                # print(f'获取用户信息失败：{json_data["info"]}')
                return f'获取用户信息失败：{json_data["info"]}'
        else:
            # print(f'获取失败（状态码：{response.status_code}）')
            return f'获取失败（状态码：{response.status_code}）'

    def get_token(self):
        response = self.get(self.token_login.format(self.username, self.passwd))
        if response.status_code == 200:
            login_info = response.json()
            if login_info['status'] == 1:
                print('登录成功')
                data = login_info['data']
                return data['uid'], data['token']
            else:
                print('登录失败')
        else:
            print(f'返回状态码:{response.status_code}')


if __name__ == '__main__':
    renren = RenRen(username, passwd, headers)
    renren.run()
