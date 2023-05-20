import pymongo
from py0314.NotifyMessage import read_config


class MymongodbClass(object):

    def __init__(self, host: str, port: int, db: str, password: str = None, user: str = None) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.connect_client = self.init_connect()

    def init_connect(self) -> object:
        if self.password:
            mongodb_url = f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/'  # 有密码连接方式
        else:
            mongodb_url = f'mongodb://{self.host}:{self.port}/'  # 无密码连接方式
        return pymongo.MongoClient(mongodb_url)

    def get_collections(self) -> list:
        result_list = self.connect_client[self.db].list_collection_names()
        return result_list

    def insert_one(self, collection_name: str, value: dict) -> str:
        col_insert = self.connect_client[self.db][collection_name].insert_one(value)
        insert_id = col_insert.inserted_id
        return insert_id

    def insert_many(self, collection_name: str, value: list) -> str:
        col_insert = self.connect_client[self.db][collection_name].insert_many(value)
        insert_ids = col_insert.inserted_ids
        return insert_ids

    def fetch_one(self, collection_name: str, filters: dict = None) -> dict:
        result = self.connect_client[self.db][collection_name].find_one(filters)
        return result

    def fetch_all(self, collection_name: str, filters: dict = None) -> list:
        results = self.connect_client[self.db][collection_name].find(filters)
        result_list = [i for i in results]
        return result_list

    def fetch_page_info(self, collection_name: str, filters: dict = None, page_size: int = 10,
                        page_no: int = 1) -> dict:
        results = self.connect_client[self.db][collection_name].find(filters).limit(page_size).skip(
            page_size * (page_no - 1))
        result_dict = {"page_size": page_size, "page_no": page_no, "data": [i for i in results]}
        return result_dict

    def fetch_count_info(self, collection_name: str, filters: dict = None) -> int:
        filters = {} if filters is None else filters
        result = self.connect_client[self.db][collection_name].count_documents(filters)
        return result

    def update_one(self, collection_name: str, filters: dict, data: dict) -> int:
        result = self.connect_client[self.db][collection_name].update_one(filter=filters, update={"$set": data})
        return result.modified_count

    def update_many(self, collection_name: str, filters: dict, data: dict) -> int:
        result = self.connect_client[self.db][collection_name].update_many(filter=filters, update={"$set": data})
        return result.modified_count

    def delete_one(self, collection_name, filters: dict) -> int:
        result = self.connect_client[self.db][collection_name].delete_one(filter=filters)
        return result.deleted_count

    def delete_many(self, collection_name: str, filters: dict) -> int:
        result = self.connect_client[self.db][collection_name].delete_many(filter=filters)
        return result.deleted_count

    def drop_collection(self, collection_name: str) -> None:
        self.connect_client[self.db][collection_name].drop()

    def __del__(self):
        self.connect_client.close()


if __name__ == '__main__':
    item_infos = read_config()['DATABASES_INFO']
    mongodb = MymongodbClass(item_infos['mongo_ip'], item_infos['mongo_port'], item_infos['mongo_db'],
                             item_infos['mongo_password'], item_infos['mongo_user'])
    data = {"姓名": "小O", "年龄": 25}
    print(mongodb.insert_one(item_infos['mongo_collection'], data))
    del mongodb
