import requests
import execjs

with open('match02.js', 'r', encoding='utf-8') as f:
    Func = execjs.compile(f.read())

all_sum = 0

for page in range(1, 6):
    headers = {}
    cookies = {"sessionid": "xxxxxxxxxxx"}
    url = "https://match2023.yuanrenxue.cn/api/match2023/2"
    params = {
        "page": str(page),
        "token": Func.call('get_token', page)
    }
    resp = requests.post(url, headers=headers, cookies=cookies, params=params)
    respDict = resp.json()
    print(respDict)
    for i in respDict['data']:
        all_sum += i['value']

print(all_sum)
