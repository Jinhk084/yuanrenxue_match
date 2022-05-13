from cgi import parse_multipart
import requests
import time
import execjs

headers = {
    "user-agent": "yuanrenxue.project",
    "cookies": "sessionid=zsl8th192izmvaq7nicphmnii4vr18nj"
}

# 打开文件加载js
with open('match_06.js', 'r', encoding='utf-8') as f:
    jsCode = f.read()
Func = execjs.compile(jsCode)

all_sum = 0
for page in range(1, 6):
    # 构造请求参数
    t = int(time.time()) * 1000
    m = Func.call('get_params', t, 1)
    q = '1' + '-' + str(t) + "|"
    # 请求数据
    url = "https://match.yuanrenxue.com/api/match/6"
    params = {
        "page": str(page),
        "m": m,
        "q": q
    }
    res = requests.get(url, headers=headers, params=params)
    print(res.text)
    for data in res.json()['data']:
        all_sum += data['value'] + data['value'] * 23

print('总金额:', all_sum)
