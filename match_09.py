import requests
import execjs
import re

all_sum = 0  # 评论数总和
headers = {
    "user-agent": "yuanrenxue.project",
}
session = requests.session()
session.headers = headers


def get_cookie():
    url = 'https://match.yuanrenxue.com/match/9'
    res = session.get(url)

    # 获取动态关键的for循环代码
    for_ = re.findall('window=new Array\(\);(.*?var m=.*?)document', res.text,
                      re.S)[0]

    # 获取动态时间戳
    decrypt_time = re.findall("decrypt.*?'(.*?)'\)", for_)[0]

    # 获取循环次数
    try:
        m = re.findall('\]\(m,(.)\);m', res.text)[0]
    except:
        m = re.findall(';m<=(.*?);m', res.text)[0]

    # 加载js代码
    with open('match_09.js', 'r', encoding='utf-8') as f:
        jsCode = f.read()
    Func = execjs.compile(jsCode)

    # 调用指定方法获取cookie
    cookie_m = Func.call('get_m', m, decrypt_time)

    # 更新cookie
    session.cookies.update({'m': cookie_m})


def get_data(page):
    global all_sum
    url = 'https://match.yuanrenxue.com/api/match/9?page=' + str(page)
    res = session.get(url)
    print(res.text)

    for data in res.json()['data']:
        all_sum += data['value']


def main():
    global all_sum
    get_cookie()  # 获取js代码，并更新cookie

    # 获取5页数据
    for page in range(1, 6):
        get_data(page)

    # print('评论平均数-->', all_sum / 50)


if __name__ == '__main__':
    main()