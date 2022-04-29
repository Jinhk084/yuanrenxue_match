import httpx
import time

'''
pip install httpx         # 支持异步
pip install httpx[http2]  # 想要支持http2.0需要额外安装
'''

client = httpx.Client(http2=True)  # 类似requests.Session()

all_sum = 0
for page in range(1, 6):
    headers = {
        'User-Agent': 'yuanrenxue.project'
    }
    cookies = {
        'sessionid': '258ci83zn4g5gr1xya3v0h2ixhcjszjg'
    }
    url = f'https://match.yuanrenxue.com/api/match/17?page={page}'
    resJson = client.get(url, headers=headers, cookies=cookies).json()
    print(resJson)
    for data in resJson['data']:
        all_sum += data['value']
    time.sleep(0.5)

print('总和: ', all_sum)
