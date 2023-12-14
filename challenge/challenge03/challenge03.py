"""
验证 cookie 中的 m 参数
astDecrypt.js 为 AST 解密之后的文件
js代码是动态的,参数加密方式是固定的
"""

import time
import requests
import execjs

with open('challenge03.js', 'r') as file:
    Func = execjs.compile(file.read())


def get_page(p):
    global Func

    timestamp = int(time.time() * 1000)
    cookie_m = Func.call('get_cookie_m', timestamp)
    response = requests.post(url='https://www.python-spider.com/api/challenge3',
                             cookies={
                                 'sessionid': 'hj4ppyiyx1lsoamps5w5hy4380n5yexn',
                                 'm': cookie_m
                             },
                             headers={
                                 'Host': 'www.python-spider.com',
                                 'pragma': 'no-cache',
                                 'cache-control': 'no-cache',
                                 'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                                 'accept': 'application/json, text/javascript, */*; q=0.01',
                                 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                 'x-requested-with': 'XMLHttpRequest',
                                 'sec-ch-ua-mobile': '?0',
                                 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                                 'sec-ch-ua-platform': '"macOS"',
                                 'origin': 'https://www.python-spider.com',
                                 'sec-fetch-site': 'same-origin',
                                 'sec-fetch-mode': 'cors',
                                 'sec-fetch-dest': 'empty',
                                 'referer': 'https://www.python-spider.com/challenge/3',
                                 'accept-language': 'zh-CN,zh;q=0.9',
                             },
                             data={
                                 'page': str(p),
                             })

    resJson = response.json()
    print(p, resJson)

    pageSum = 0
    for item in resJson['data']:
        pageSum += int(item['value'].strip())

    return pageSum


if __name__ == '__main__':
    pageSum100 = 0
    for page in range(1, 101):
        pageSum100 += get_page(page)
    print("100 page sum: ", pageSum100)
