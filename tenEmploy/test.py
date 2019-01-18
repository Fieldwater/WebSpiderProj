from pymongo import MongoClient

#实例化
client = MongoClient(host="127.0.0.1", port=27017)
collection = client["test"]["t100"]

# #插入数据
collection.insert({"name": "Field", "age": 18})
# #插入多个数据
data_list = [{"name":"test{}".format(i)} for i in range(10)]
collection.insert_many(data_list)

# #查询一个记录
t = collection.find_one({"name":"Field"})
print(t)
# #查询所有记录
t_all = collection.find({"name": "Field"})
print(t_all)

# 更新
collection.update_one({"name": "test100"}, {"$set": {"name":"new100"}})
collection.update_many({"name":"test200"}, {"$set":{"name":"new200"}})

# 删除
collection.delete_one()
collection.delete_many(list)