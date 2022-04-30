import requests
import execjs

headers = {
    "user-agent": "yuanrenxue.project",
}
cookies = {
    'sessionid': '97693zipil9py4evxtw4oj7sd5f4nhdq'
}
url = "https://match.yuanrenxue.com/api/match/1"

# 打开js文件
with open('match_01.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
func = execjs.compile(js_code)

all_sum = 0
for page in range(1, 6):
    m = func.call('get_m')
    params = {
        "page": str(page),
        "m": m
    }
    res = requests.get(url, headers=headers, cookies=cookies, params=params)
    # 求和
    for data in res.json()['data']:
        all_sum += data['value']
    print(res.text)

print('平均值:', all_sum / 50)  # 4700.0 --> 4700(注意小数点)
