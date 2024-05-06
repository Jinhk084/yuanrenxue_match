import requests
import execjs

session = requests.session()
session.cookies.update({'sessionid': 'lxdi3c0hyhn2ngjqqf3kjfijeuwyfetp'})

with open('./match01.js', 'r') as file: Func = execjs.compile(file.read())

all_sum = 0
for page in range(1, 6):
    params = Func.call('get_params', page)
    resp = session.post(url="https://match2023.yuanrenxue.cn/api/match2023/1",
                        data={
                            'page': params['page'],
                            'token': params['token'],
                            'now': params['now']
                        })

    resp_json = resp.json()
    print(resp_json)

    for value in resp_json['data']:
        all_sum += value['value']

print('5页总和:', all_sum)
