import requests
import execjs
'''
注意delete window和n.g的执行流程
'''

headers = {
    "user-agent": "yuanrenxue.project",
    'Cookie': 'sessionid=4isxukvsmc57etqgruja6qq22341xb7j'
}
url = "https://match.yuanrenxue.com/api/match/16"
# 打开js代码并加载
with open('match_16.js', 'r', encoding='utf-8') as f:
    jsCode = f.read()
Func = execjs.compile(jsCode)

# 翻页求和
all_sum = 0
for page in range(1, 6):
    arg = Func.call('get_params')
    params = {"page": str(page), "m": arg['m'], "t": arg['t']}
    res = requests.get(url, headers=headers, params=params)
    print(res.text)

    # 求和
    for data in res.json()['data']:
        all_sum += data['value']

print('5页总和: ', all_sum)
