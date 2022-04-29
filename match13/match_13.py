import requests
import re
import time

'''
如果是登陆用户,第一次请求cookie加密密文的时候,需要带上登陆信息sessionid,才能访问到正确的cookie加密密文
'''

session = requests.session()
headers = {
    'User-Agent': 'yuanrenxue.project',
}
cookies_id = {
    'sessionid': '258ci83zn4g5gr1xya3v0h2ixhcjszjg'
}
session.cookies.update(cookies_id)
session.headers = headers

# 获取设置cookie的js代码
url = "https://match.yuanrenxue.com/match/13"
cookieJsCode = session.get(url).text

# 匹配出cookie值,并更新
cookie = ''.join(re.findall("\('(.)'\)", cookieJsCode))
key, value = cookie.split('=')
session.cookies.update({key: value})

# 请求数据
all_sum = 0
for page in range(1, 6):
    url_api = f'https://match.yuanrenxue.com/api/match/13?page={page}'
    res_data = session.get(url_api).json()
    print(res_data)
    # 求和
    for i in res_data['data']:
        all_sum += i['value']
    time.sleep(0.5)

print('总和: ', all_sum)
