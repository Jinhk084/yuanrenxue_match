import requests

session = requests.session()


def get_page(p):
    global session

    session.headers.update({
        'authority': 'www.python-spider.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'sessionid=hj4ppyiyx1lsoamps5w5hy4380n5yexn; sign=wvbxzhldct',
        'origin': 'https://www.python-spider.com',
        'pragma': 'no-cache',
        'referer': 'https://www.python-spider.com/challenge/6',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    })
    session.cookies.update({'sessionid': 'hj4ppyiyx1lsoamps5w5hy4380n5yexn'})
    response = session.post(url='https://www.python-spider.com/api/challenge6',
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
