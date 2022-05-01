import requests

headers = {
    'Host': 'match.yuanrenxue.com',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'yuanrenxue.project',
    'Accept': '*/*',
    'Origin': 'https://match.yuanrenxue.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://match.yuanrenxue.com/match/3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'sessionid=f7clla3nfe7j79bnmdcobpja168ycjm9'
}

session = requests.session()
session.headers = headers

data_list = []
for page in range(1, 6):
    # 访问jssm
    res_1 = session.post('https://match.yuanrenxue.com/jssm')
    # 访问数据接口
    url = "https://match.yuanrenxue.com/api/match/3"
    params = {
        "page": str(page)
    }
    res = session.get(url, params=params)
    print(res.text)
    # 添加
    for data in res.json()['data']:
        data_list.append(data['value'])

print(data_list)
print('频率最高的数: ', max(data_list, key=data_list.count))  # 8717
