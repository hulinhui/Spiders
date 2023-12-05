import logging

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
        self.login_url = 'https://www.kejiwanjia.com/wp-json/jwt-auth/v1/token'
        self.sign_url = 'https://www.kejiwanjia.com/wp-json/b2/v1/userMission'
        self.submit_url = 'https://www.kejiwanjia.com/wp-json/b2/v1/commentSubmit'

    def get_userinfo(self):
        user_list = [
            {
                "username": "2055957056@qq.com",
                "password": "hlh123456"
            }, {
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
            fh = logging.FileHandler('log.txt', mode='w', encoding='utf-8')
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
        current_level = userdata['lv']['lv']['name']
        credit = userdata['lv']['lv']['credit']
        next_level = userdata['lv']['lv']['lv_next_name']
        next_credit = userdata['lv']['lv']['lv_next_credit']
        lv_ratio = 100 - int(userdata['lv']['lv']['lv_ratio'])
        post_count = userdata['post_count']
        followers = userdata['followers']
        following = userdata['following']
        comment_count = userdata['comment_count']
        text1 = f'登录情况：【{name}】登录成功;'
        text2 = f'当前用户等级为:{current_level},总共{credit}个积分;'
        text3 = f'下一级等级为:{next_level},需要{next_credit}积分,距离下一级进度还差{lv_ratio}%;'
        text4 = f'当前用户发布了{post_count}篇文章,有{followers}个粉丝,关注了{following}人，评论了{comment_count}个文章。'
        return text1, text2, text3, text4

    def login(self, data):
        session = requests.Session()
        data = {"username": data['username'], "password": data['password']}
        response = session.post(
            url=self.login_url,
            data=data
        )
        json_data = response.json()
        if response.status_code == 200:
            self.headers['authorization'] = f'Bearer {json_data["token"]}'
            self.logger.info(self.get_user(json_data)[0])
            self.logger.info(self.get_user(json_data)[1])
            self.logger.info(self.get_user(json_data)[2])
            self.logger.info(self.get_user(json_data)[3])
            return session
        else:
            self.logger.info(f'登录情况：登录失败,原因:{json_data["message"]}')

    def sign(self, s):
        response = s.post(self.sign_url, headers=self.headers)
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

    def comment_submit(self, s):
        ###data={"comment_post_ID":"","author":"","comment":"","comment_parent":""}
        pass

    def main(self):
        self.logger.info('科技玩家信息如下：')
        for item in self.get_userinfo():
            session = self.login(item)
            if session:
                # 2、签到
                self.sign(session)
                self.comment_submit(session)
                self.logger.info('==========================')
        send_ding('科技玩家签到', mode=0)


if __name__ == '__main__':
    kjwj = KeJiWanJia()
    kjwj.main()
