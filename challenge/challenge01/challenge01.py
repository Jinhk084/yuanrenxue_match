"""
主要验证请求headers 的 safe和timestamp对应关系
"""

import base64
import requests
import time
import hashlib


def encode_base64(string):
    encoded_bytes = base64.b64encode(string.encode())
    encoded_string = encoded_bytes.decode()
    return encoded_string


def md5_digest(string):
    md5_hash = hashlib.md5(string.encode())
    return md5_hash.hexdigest()


def get_page(p):
    timestamp = str(int(time.time()))
    base64Str = encode_base64("9622" + timestamp)
    safe = md5_digest(base64Str)

    response = requests.post(url='https://www.python-spider.com/api/challenge1',
                             cookies={
                                 'sessionid': 'hj4ppyiyx1lsoamps5w5hy4380n5yexn',
                             },
                             headers={
                                 'authority': 'www.python-spider.com',
                                 'accept': 'application/json, text/javascript, */*; q=0.01',
                                 'accept-language': 'zh-CN,zh;q=0.9',
                                 'cache-control': 'no-cache',
                                 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                 'origin': 'https://www.python-spider.com',
                                 'pragma': 'no-cache',
                                 'referer': 'https://www.python-spider.com/challenge/1',
                                 'safe': safe,
                                 'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                                 'sec-ch-ua-mobile': '?0',
                                 'sec-ch-ua-platform': '"macOS"',
                                 'sec-fetch-dest': 'empty',
                                 'sec-fetch-mode': 'cors',
                                 'sec-fetch-site': 'same-origin',
                                 'timestamp': timestamp,
                                 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                                 'x-requested-with': 'XMLHttpRequest',
                             },
                             data={
                                 'page': str(p)
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
