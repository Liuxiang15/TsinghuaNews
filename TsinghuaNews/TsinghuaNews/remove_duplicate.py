#本文件删除title或者url重复的数据，同时清除content和date为空的数据
import pymongo
mongo_host = "localhost"
mongo_port = 27017
mongo_db_name = "TsinghuaNews"
mongo_db_collection = "THUNewsUrl"
client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
mydb = client[mongo_db_name]
articles = mydb[mongo_db_collection].find()

result = set()
return_res = []
mydb[mongo_db_collection].remove({"content":""})
mydb[mongo_db_collection].remove({"date":""})
for data in articles:
    if data["title"] in result:
        mydb[mongo_db_collection].remove({"title":data["title"]})
        mydb[mongo_db_collection].insert(data)
        continue
    return_res.append(data)
    result.add(data["title"])
 print("执行完成")

