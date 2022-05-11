import requests
import execjs
import numpy as np

headers = {
    "user-agent": "yuanrenxue.project",
}
cookies = {
    "sessionid": "we6oumc7gkkbyyhxggmwc4sol0g38k1g",
}
url = "https://match.yuanrenxue.com/api/match/5"

with open('match_05.js', 'r', encoding='utf-8') as f:
    jsCode = f.read()

Func = execjs.compile(jsCode)
par = Func.call('get_params')
# 更新cookie
cookies['RM4hZBv0dDon443M'] = par['RM4hZBv0dDon443M']

allData = []
for page in range(1, 6):
    params = {
        "page": str(page),
        "m": par['url_m'],
        "f": par['url_m']
    }
    res = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(res.text)
    for data in res.json()['data']:
        allData.append(data['value'])

max5 = np.sort(allData)[-5:]  # 升序
print('5名直播间热度的加和:', sum(max5))
