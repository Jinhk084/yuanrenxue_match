import requests
import base64
import time

headers_ = {
    'User-Agent': 'yuanrenxue.project'
}
cookies_ = {
    'sessionid': 'za98k9j6qyod2tskv7y2cz8cuqpg8zmz'
}
all_sum = 0
for page in range(1, 6):
    m = 'yuanrenxue' + str(page)
    m_b64 = base64.b64encode(m.encode()).decode('utf-8')
    # 请求的url
    url = f'http://match.yuanrenxue.com/api/match/12?page={page}&m={m_b64}'
    res_data = requests.get(url, headers=headers_, cookies=cookies_).json()
    print(res_data)
    # 求和
    for i in res_data['data']:
        all_sum += i['value']
    time.sleep(0.5)

print('总和:', all_sum)
