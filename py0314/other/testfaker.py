import random

from faker import Faker
from py0314.NotifyMessage import read_config
from py0314.connectmondb import MymongodbClass


def get_random_data():
    data_list = []
    faker = Faker(locale='zh_CN')
    for _ in range(30):
        item_data = {'姓名': faker.name(), '性别': random.choice(['男', '女']), '年龄': random.randint(18, 45),
                     '手机号': faker.phone_number(), '身份证号': faker.ssn(min_age=18, max_age=45), '工作': faker.job(),
                     '地址': faker.address()}
        data_list.append(item_data)
    return data_list


def main():
    item_infos = read_config()['DATABASES_INFO']
    mongodb = MymongodbClass(item_infos['mongo_ip'], item_infos['mongo_port'], item_infos['mongo_db'],
                             item_infos['mongo_password'], item_infos['mongo_user'])
    # data_list = get_random_data()
    data = {"年龄": 101}
    result = mongodb.update_many('info_collection', filters={"性别": "女"}, data=data)
    print(f'{result}条数据修改成功！')


if __name__ == '__main__':
    main()
