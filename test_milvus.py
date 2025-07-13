from pymilvus import connections, utility

connections.connect(host="localhost", port="19530")
print(utility.list_collections())  # 成功应返回 []
print("Milvus 连接成功！")