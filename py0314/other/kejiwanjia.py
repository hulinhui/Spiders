import json
import logging
import re
import time

import requests
from py0314.NotifyMessage import send_ding


class KeJiWanJia(object):
    """docstring for KeJiWanJia"""

    def __init__(self):
        super(KeJiWanJia, self).__init__()
        self.logger = self.get_logging()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4613.0 Safari/537.36 Edg/95.0.1000.0',
            'accept': 'application/json, text/plain, */*'}
        self.login_url = 'https://www.kejiwanjia.net/wp-json/jwt-auth/v1/token'
        self.sign_url = 'https://www.kejiwanjia.net/wp-json/b2/v1/userMission'
        self.submit_url = 'https://www.kejiwanjia.net/wp-json/b2/v1/commentSubmit'
        self.PostList = 'https://www.kejiwanjia.net/wp-json/b2/v1/getModulePostList'
        self.task_url = 'https://www.kejiwanjia.net/wp-json/b2/v1/getTaskData'
        self.user_list_url = 'https://www.kejiwanjia.net/page/5?s&type=user'
        self.check_follow = 'https://www.kejiwanjia.net/wp-json/b2/v1/checkFollowByids'
        self.AuthorFollow_url = 'https://www.kejiwanjia.net/wp-json/b2/v1/AuthorFollow'

    def get_userinfo(self):
        user_list = [
            {
                "username": "2055957056@qq.com",
                "password": "hlh123456"
            }
            ,
            {
                "username": "975081281@qq.com",
                "password": "hlh123456"
            }
        ]
        return user_list

    def get_logging(self):
        # 1、创建一个logger
        logger = logging.getLogger()
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            # 2、创建一个handler，用于写入日志文件
            fh = logging.FileHandler('log.txt', mode='w',
                                     encoding='utf-8')
            # 3、定义handler输出格式
            fh.setFormatter(logging.Formatter('%(message)s'))
            # 4、将logger添加到handler
            logger.addHandler(fh)

            # 1、创建一个handler，用于写入日志文件
            ch = logging.StreamHandler()
            # 2、定义handler输出格式
            ch.setFormatter(logging.Formatter('[%(asctime)s]:%(levelname)s:%(message)s'))
            # 3、将logger添加到handler
            logger.addHandler(ch)

        return logger

    def get_user(self, userdata):
        name = userdata['name']
        self.name = name
        current_level = userdata['lv']['lv']['name']
        credit = userdata['credit']
        next_level = userdata['lv']['lv']['lv_next_name']
        lv_ratio = 100 - int(userdata['lv']['lv']['lv_ratio'])
        post_count = userdata['post_count']
        followers = userdata['followers']
        following = userdata['following']
        comment_count = userdata['comment_count']
        text1 = f'登录情况：【{name}】登录成功;'
        text2 = f'当前用户等级为:{current_level},总共{credit}个积分;'
        text3 = f'下一级等级为:{next_level},距离下一级进度还差{lv_ratio}%;'
        text4 = f'当前用户发布了{post_count}篇文章,有{followers}个粉丝,关注了{following}人，评论了{comment_count}个文章。'
        return text1, text2, text3, text4

    ###登录####
    def login(self, data):
        response = requests.post(
            url=self.login_url,
            data=data
        )
        print(response.request.headers)
        print(response.headers)
        json_data = response.json()
        if response.status_code == 200:
            cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
            self.headers['authorization'] = f'Bearer {json_data["token"]}'
            self.headers['cookie'] = f'b2_token={cookies_dict["b2_token"]}'
            self.logger.info(self.get_user(json_data)[0])
            self.logger.info(self.get_user(json_data)[1])
            self.logger.info(self.get_user(json_data)[2])
            self.logger.info(self.get_user(json_data)[3])
        else:
            self.logger.info(f'登录情况：登录失败,原因:{json_data["message"]}')

    ######签到#######
    def sign(self):
        response = requests.post(self.sign_url, headers=self.headers)
        if response.status_code == 200:
            json_data = response.json()
            if type(json_data) != str:
                sign_date = json_data['mission']['date']
                sign_score = json_data['mission']['credit']
                sign_day = json_data['mission']['always']
                sum_score = json_data['mission']['my_credit']
                self.logger.info(f'签到情况:签到成功')
                self.logger.info(f'签到时间:{sign_date}')
                self.logger.info(f'本次签到获得:{sign_score}分')
                self.logger.info(f'连续签到天数:{sign_day}天;签到后积分:{sum_score}分')
            else:
                self.logger.info('签到情况:你今天已经签到过了')
        else:
            self.logger.info("签到情况:签到失败!")

    ##评论任务###
    def getTaskData(self, field):
        try:
            response = requests.post(self.task_url, headers=self.headers)
            response.encoding = 'utf-8'
            response.raise_for_status()
            finish_num = int(response.json()['task'][field]['finish'])
            time_num = int(response.json()['task'][field]['times'])
            post_id = response.json()['task'][field]['url'].split('/')[-1].split('.')[0]
            return post_id, finish_num, time_num
        except Exception as e:
            self.logger.info('任务列表获取失败')

    def submit_content(self, post_id):
        data = {"comment_post_ID": post_id, "author": self.name, "comment": "谢谢分享~", "comment_parent": "0"}
        response = requests.post(self.submit_url, headers=self.headers, data=data)
        if response.status_code == 200:
            return 'succ'
        elif response.status_code == 403:
            return 'Flag'
        else:
            return 'fail'

    def comment_submit(self):
        task_data = self.getTaskData('task_comment')
        if task_data:
            post_id, finish_num, time_num = task_data
            while finish_num < time_num:
                if self.submit_content(post_id) == 'succ':
                    self.logger.info(f'{post_id}：评论成功,奖励20经验值')
                    task_data = self.getTaskData('task_comment')
                    post_id = task_data[0]
                    finish_num = task_data[1]
                    time_num = task_data[2]
                elif self.submit_content(post_id) == 'Flag':
                    self.logger.info('评论提交速度过快，等待5s')  # 防止提交速度过快
                else:
                    self.logger.info(f'{post_id}：评论失败,开始下一篇文章评论。。')
                    task_data = self.getTaskData('task_comment')
                    post_id = task_data[0]
                    finish_num = task_data[1]
                    time_num = task_data[2]
                time.sleep(3)

            self.logger.info('恭喜你，完成了评论任务！！')

    #####关注任务#####

    def get_user_list(self):
        resp = requests.get(self.user_list_url, headers=self.headers)
        if resp.status_code == 200:
            user_data = re.findall('b2_search_data = (.*?);', resp.text)[0]
            user_data_dict = json.loads(user_data)
            return user_data_dict['users']
        else:
            self.logger.info('获取user列表失败')

    def checkFollowByids(self, data_list):
        data = {f'ids[{i}]': data_list[i] for i in range(16)}
        resp = requests.post(self.check_follow, headers=self.headers, data=data)
        if resp.status_code == 200:
            user_id_list = [user[0] for user in resp.json().items() if not user[1]]
            return user_id_list
        else:
            self.logger.info('check检查接口查询失败')

    def AuthorFollow_api(self, user):
        resp = requests.post(self.AuthorFollow_url, headers=self.headers, data={'user_id': user})
        if resp.status_code == 200:
            return resp.text
        elif resp.status_code == 403:
            return 403
        else:
            self.logger.info('关注接口返回失败')

    def AuthorFollow(self):
        user_list = self.get_user_list()
        user_id_list = self.checkFollowByids(user_list)
        if len(user_id_list) >= 5:
            _, finish_num, time_num = self.getTaskData('task_follow')
            while finish_num < time_num:
                if self.AuthorFollow_api(user_id_list[finish_num]) == 'true':
                    self.logger.info(f'{user_id_list[finish_num]}：关注成功,奖励5经验值')
                    task_data = self.getTaskData('task_follow')
                    finish_num = task_data[1]
                    time_num = task_data[2]
                elif self.AuthorFollow_api(user_id_list[finish_num]) == 403:
                    self.logger.info('关注用户速度过快，等待3s')  # 防止提交速度过快
                    time.sleep(3)
                else:
                    self.logger.info(f'{user_id_list[finish_num]}：关注失败,再次关注')
                    task_data = self.getTaskData('task_follow')
                    finish_num = task_data[1]
                    time_num = task_data[2]
            self.logger.info('恭喜你，完成了关注任务！！')
        else:
            self.logger.info('当前页useid不足5个，无法完成关注任务')

    def main(self):
        self.logger.info('科技玩家信息如下：')
        for item in self.get_userinfo():
            self.login(item)
            if self.headers.get('authorization'):
                # 2、签到
                # self.sign()
                # 评论
                # self.comment_submit()
                self.logger.info('==========================')
                # 关注
                # self.AuthorFollow()
                self.logger.info('==========================')
                del self.headers['authorization']
                del self.headers['cookie']
        send_ding('科技玩家签到', mode=0)


if __name__ == '__main__':
    kjwj = KeJiWanJia()
    kjwj.main()
