import json

# 读取 JSON 文件
file_path = 'C:\\Users\\Administrator\\Desktop\\example.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# 处理数据
print("name:", data["name"])
print("resolution:", data["resolution"])
print("matchCount:", data["matchCount"])