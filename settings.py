import pymongo


class MongoPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient(
            '127.0.0.1',
            27017
        )
        db = self.conn["cathay"]  # database
        self.collection = db['591_house']  # table

    def process_item(self, house_info):
        self.collection.insert(vars(house_info))
        return house_info

    def process_items(self, house_info_list):
        data = [vars(house) for house in house_info_list]
        self.collection.insert_many(data)
        return house_info_list

    def get_houses(self, number):
        myquery = {"phone_num": number}
        return self.collection.find(myquery)
