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

    def get_houses(self, number=None, gender_limit=None, role=None, districts=None):
        myquery = {"phone_num": number} if number else {}
        if gender_limit:
            if gender_limit == "male":
                myquery["gender_limit"] = {"$ne": "限女"}
            elif gender_limit == "female":
                myquery["gender_limit"] = {"$ne": "限男"}

        if role:
            if role == "屋主":
                myquery["role"] = role
            elif role == "非屋主":
                myquery["role"] = {"$ne": "屋主"}
        if districts:
            myquery["district"] = {"$in": districts}
        return self.collection.find(myquery)
