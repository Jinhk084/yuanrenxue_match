import requests
import execjs
import time

with open('./match03.js', 'r', encoding='utf-8') as f:
    Func = execjs.compile(f.read())

session = requests.session()
session.cookies.update({'sessionid': 't9miyqx2vn03h63lm5h0fy0jd1dkrdsc'})

all_sum = 0
for page in range(1, 6):
    timestamp = int(time.time() * 1000)

    session.headers.update({'accept-time': str(timestamp)})
    token = Func.call('sm3Digest', f'{timestamp}{page}')
    resp = session.post(url="https://match2023.yuanrenxue.cn/api/match2023/3",
                        data={'page': page,
                              'token': token})

    respDict = resp.json()
    print(respDict)
    for i in respDict['data']:
        all_sum += i['value']

print('5页总和:',all_sum)

