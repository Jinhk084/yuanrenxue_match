"""
请求返回: <script>var x="div@Expires@@captcha@while@length@..... 等内容是烟雾弹, 浏览器正常访问是没有返回的这个的
访问逻辑解决:
    1.不仅要解决: https://match.yuanrenxue.cn/jssm 的问题
    2.也要解决请求: https://match.yuanrenxue.cn/api/match/3 请求头的顺序问题
    3.请求头顺序要和浏览器或者抓包工具里面的顺序一致, 推荐手动复制, 验证的时候添加本地代理抓包进行确认!
不知是否是模块版本问题还是python版本: 以前可以使用 requests 库的 session 来控制请求头顺序
采用httpx也可以解决
"""

import httpx
import json

globalItem = []


def main():
    global globalItem

    session = httpx.Client()
    session.headers.update({
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://match.yuanrenxue.cn/match/3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'sessionid=4eb8i3c2anwrkqzignb4cywaw7mnwspg',
    })

    for page in range(1, 6):
        resp1 = session.post('https://match.yuanrenxue.cn/jssm')
        resp2 = session.get('https://match.yuanrenxue.cn/api/match/3', params={"page": str(page)})
        print(resp2.text)
        dataJson = json.loads(resp2.text)

        for item in dataJson['data']:
            globalItem.append(item['value'])

    session.close()


if __name__ == '__main__':
    main()
    most_common_element = max(globalItem, key=globalItem.count)  # 获取出现频率最高的
    print(most_common_element)
