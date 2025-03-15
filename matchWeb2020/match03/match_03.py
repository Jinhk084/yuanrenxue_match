"""
访问逻辑解决:
    1.做好请求头顺序的把控,推荐配合抓包软件,获取正确的顺序后构建请求
        请求头顺序要和浏览器或者抓包工具里面的顺序一致,推荐手动复制,验证的时候添加本地代理抓包进行确认!
    2.https://match.yuanrenxue.cn/jssm 的问题:
        该接口请求正确会返回一个cookie,请求失败则不返回
    3.https://match.yuanrenxue.cn/api/match/3 的问题:
        如果返回: <script>var x="div@Expires@@captcha@while@length@..... 等内容是烟雾弹,浏览器正常访问是没有返回的这个的
"""

from matchWeb2020.config import BASE_URL, get_session, verify_answers, SESSION_ID

session = get_session()
session.cookies.clear()
session.headers.update({
    "content-length": "0",
    "sec-ch-ua-platform": "\"macOS\"",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?0",
    "accept": "*/*",
    "origin": "https://match.yuanrenxue.cn",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://match.yuanrenxue.cn/match/3",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "priority": "u=0, i",
    "Cookie": f'sessionid={SESSION_ID}',
})

items = []
for page in range(1, 6):
    resp1 = session.post(url=f'{BASE_URL}/jssm')
    if not resp1.cookies.values():
        raise Exception('访问: /jssm 未通过')

    resp2 = session.get(url=f'{BASE_URL}/api/match/3',
                        params={"page": str(page)})
    if "status" not in resp2.text:
        raise Exception('访问: /api/match/3 未通过')

    resp_json = resp2.json()
    print(page, resp_json)
    [items.append(item['value']) for item in resp_json['data']]

most_common_element = max(items, key=items.count)
print(f'频率最高: {most_common_element}')
verify_answers(session, most_common_element, 3)
