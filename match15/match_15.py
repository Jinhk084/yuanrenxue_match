import requests
import math
import random
import time
import pywasm  # pip install pywasm

headers = {
    'User-Agent': 'yuanrenxue.project',
    'Cookie': 'sessionid=mjjtd90ctnt3nrtbrzlw6k6ydd4ur05f'
}

url = "https://match.yuanrenxue.com/api/match/15"

all_sum = 0
for page in range(1, 6):
    # 获取m参数
    t = int(time.time())
    t1 = int(t / 2)
    t2 = int(t / 2 - math.floor(random.random() * 50 + 1))
    Func = pywasm.load("main.wasm")
    t0 = Func.exec("encode", [t1, t2])

    params = {
        "m": f"{t0}|{t1}|{t2}",
        "page": str(page)
    }
    res = requests.get(url, headers=headers, params=params)
    # 求和
    for data in res.json()['data']:
        all_sum += data['value']
    print(res.text)

# print('5页总和: ', all_sum)
