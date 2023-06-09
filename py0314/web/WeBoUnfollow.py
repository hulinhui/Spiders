import requests


class WeiBoFollow:

    def __init__(self, cookies_str):
        self.follow_url = 'https://weibo.com/ajax/profile/followContent?'
        self.unfollow_url = 'https://weibo.com/ajax/friendships/destory'
        self.special_follow_url = 'https://weibo.com/ajax/friendships/specialAdd'
        self.headers, self.cookies = self._get_cookies_item(cookies_str)
        self.file_obj = self._get_file_object()
        self.follow_item = {}

    @staticmethod
    def _get_file_object(mode='r'):
        return open('关注列表.txt', mode=mode, encoding='utf-8')

    @staticmethod
    def _get_cookies_item(data):
        headers = {
            'origin': 'https://weibo.com',
            'referer': 'https://weibo.com/u/page/follow/6192568630',
            'server-version': 'v2023.05.06.1',
            'traceparent': '00-accb6b7f46203b1b36dab604ccbc0b97-6043ffcce5b16a37-00',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': 'wpm_U-W7469B0hrz3GvsHT9w'
        }
        cookies_item = {data_str.split('=')[0].strip(): data_str.split('=')[1] for data_str in data.split(';') if
                        data_str}
        return headers, cookies_item

    def _get_href(self, url_link, method='get', data_params=None, data=None):
        try:
            response = requests.request(url=url_link, method=method, params=data_params, data=data,
                                        headers=self.headers, cookies=self.cookies)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response
        except Exception as e:
            print(e)

    def _get_follow_data(self):
        page_num = 1
        next_cursor = None
        while True:
            params = {'page': page_num, 'next_cursor': next_cursor}
            response = self._get_href(self.follow_url, data_params=params)
            if response:
                json_data = response.json()
                if json_data.get('ok'):
                    follows_json = json_data['data']['follows']
                    self.follow_item.update({follows['name']: follows['id'] for follows in follows_json['users']})
                    # self.file_obj.write('\n'.join([follows['name'] for follows in follows_json['users']]))
                    if not follows_json['next_cursor']:
                        break
                    next_cursor = follows_json['next_cursor']
                    page_num += 1
                else:
                    print('获取关注列表数据失败！')
                    break
            else:
                print('获取关注列表数据失败！')
                break

    def unfollow_data(self, follow_id):
        params = {"uid": follow_id}
        response = self._get_href(self.unfollow_url, method='post', data=params)
        if response:
            json_data = response.json()
            if not json_data['following']:
                print('取消关注成功')
            else:
                print('取消关注失败')
        else:
            print('取消关注接口失败')

    def special_follow(self, follow_id):
        params = {"touid": follow_id}
        response = self._get_href(self.special_follow_url, method='post', data=params)
        if response:
            json_data = response.json()
            if json_data['result']:
                print('特殊关注成功！')
            else:
                print('特殊关注失败！')
        else:
            print('特殊关注接口失败！')

    def unfollow(self):
        self._get_follow_data()
        white_list = self.file_obj.read().split('\n')
        if white_list and self.follow_item:
            count = 0
            special_count = 0
            for follow_name in self.follow_item:
                if follow_name in white_list:
                    self.special_follow(self.follow_item[follow_name])
                    special_count += 1
                    continue
                self.unfollow_data(self.follow_item[follow_name])
                count += 1
            else:
                print(f'总共取关{count}个,设置特殊关注{special_count}个')

    def __del__(self):
        self.file_obj.close()


if __name__ == '__main__':
    cookies_str = 'SINAGLOBAL=3688093357847.5815.1679994508997; UOR=,,hi.kejiwanjia.com; SSOLoginState=1682319367; XSRF-TOKEN=wpm_U-W7469B0hrz3GvsHT9w; _s_tentry=weibo.com; Apache=6751687419123.54.1683362162915; ULV=1683362162980:2:1:1:6751687419123.54.1683362162915:1679994509102; SCF=AjPfOgBWM5kKQkAN1wjoGvqwbx5zFTmonmUHxGqgsN11WhkJsV3c5nIGewSjaCBZw1ifTLvyCFSjcipMUnaIO9k.; SUB=_2A25JXBEEDeRhGeBP4lAU9ibKyDyIHXVqKAXMrDV8PUNbmtAGLWHikW9NRCPTJ4cbzFh6JtoY6YPu0im_dUNIFWtT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56Ww3L8_-XbTK0sOLbKFNa5JpX5KzhUgL.Foqp1KzfSonce052dJLoIpvki--Xi-ihi-zpi--NiKyFi-zRi--NiKyhi-8FKg8k; ALF=1715049684; WBPSESS=x_I30mfugLX89Ayob7-5a95rmHCLR3PwKr4jpPOFkTZW5u5zLYgYFLwOiA3XWmYVIssTBec9FnC84ZHi0qmleaJskgFf6qLdCbZ8A7OzQqVEM-XuXI65rThpQWpIwmVTe2rQJfyP63mXY6qhUKa1Fw=='
    weibo = WeiBoFollow(cookies_str)
    weibo.unfollow()
