import requests
import execjs
import re

headers = {
    "user-agent": "yuanrenxue.project",
}

cookies = {
    "sessionid":
    "xj9cs7zx1wxkfxwlq6bxmiubgosvol3t",
    "mz":
    "TW96aWxsYSxOZXRzY2FwZSw1LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84Ni4wLjQyNDAuMTk4IFNhZmFyaS81MzcuMzYsW29iamVjdCBOZXR3b3JrSW5mb3JtYXRpb25dLHRydWUsLFtvYmplY3QgR2VvbG9jYXRpb25dLDEyLHpoLUNOLHpoLUNOLHpoLDAsW29iamVjdCBNZWRpYUNhcGFiaWxpdGllc10sW29iamVjdCBNZWRpYVNlc3Npb25dLFtvYmplY3QgTWltZVR5cGVBcnJheV0sdHJ1ZSxbb2JqZWN0IFBlcm1pc3Npb25zXSxXaW4zMixbb2JqZWN0IFBsdWdpbkFycmF5XSxHZWNrbywyMDAzMDEwNyxbb2JqZWN0IFVzZXJBY3RpdmF0aW9uXSxNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXT1c2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg2LjAuNDI0MC4xOTggU2FmYXJpLzUzNy4zNixHb29nbGUgSW5jLiwsW29iamVjdCBEZXByZWNhdGVkU3RvcmFnZVF1b3RhXSxbb2JqZWN0IERlcHJlY2F0ZWRTdG9yYWdlUXVvdGFdLDEwODAsNjIsMCwxODU4LDI0LDEwODAsW29iamVjdCBTY3JlZW5PcmllbnRhdGlvbl0sMjQsMTkyMCxbb2JqZWN0IERPTVN0cmluZ0xpc3RdLGZ1bmN0aW9uIGFzc2lnbigpIHsgW25hdGl2ZSBjb2RlXSB9LCxtYXRjaC55dWFucmVueHVlLmNvbSxtYXRjaC55dWFucmVueHVlLmNvbSxodHRwczovL21hdGNoLnl1YW5yZW54dWUuY29tL21hdGNoLzE0LGh0dHBzOi8vbWF0Y2gueXVhbnJlbnh1ZS5jb20sL21hdGNoLzE0LCxodHRwczosZnVuY3Rpb24gcmVsb2FkKCkgeyBbbmF0aXZlIGNvZGVdIH0sZnVuY3Rpb24gcmVwbGFjZSgpIHsgW25hdGl2ZSBjb2RlXSB9LCxmdW5jdGlvbiB0b1N0cmluZygpIHsgW25hdGl2ZSBjb2RlXSB9LGZ1bmN0aW9uIHZhbHVlT2YoKSB7IFtuYXRpdmUgY29kZV0gfQ=="
}

session = requests.session()
session.headers = headers
session.cookies.update(cookies)

all_sum = 0


def get_js():
    # 请求js代码
    url = "https://match.yuanrenxue.com/api/match/14/m"
    res = session.get(url)
    res_text = res.text

    # 替换本地卡死的关键代码
    setInterval = re.findall('setInterval.*?0x.{3}\)', res_text)[0]  # 匹配出定时器
    func = re.findall('\);(.*?);window', res_text)[0][-12:]  # 匹配出函数的执行

    # 替换原js文件
    new_js = res_text.replace(setInterval, '').replace(func, '')

    # 构造代码运行环境
    jsCode = 'window = {};' + new_js + ';function get_v14_v142(){ return window }'
    result = execjs.compile(jsCode).call('get_v14_v142')

    # 取值
    v14 = result['v14']
    v142 = result['v142']

    return v14, v142


def get(v14, v142, page):
    global all_sum
    # 打开本地抠出来的js文件
    with open('match_14.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    # 构造最终的js代码
    js_code = '''
        window = global;
        navigator = {
            appName:"Netscape",
            cajaVersion:undefined,
            userAgent:"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            cookieEnabled:true,
            appCodeName:"Mozilla"
        }
        CanvasCaptureMediaStreamTrack = function(){};
        ''' + ';window.n = 0;window.v14 = "' + v14 + '"; window.v142 = ' + v142 + js_code
    # print(js_code)

    # 加载js获取cookie
    cookie_m = execjs.compile(js_code).call('get_m', page)

    # 更新cookie
    session.cookies.update({'m': cookie_m})

    # 请求数据
    url = 'https://match.yuanrenxue.com/api/match/14?page=' + str(page)
    res = session.get(url)
    print(res.text)

    # # 求和操作
    # for data in res.json()['data']:
    #     all_sum += data['value']


def main():
    for page in range(1, 6):
        # 获取全局变量v14和v142
        v14, v142 = get_js()
        # 获取数据
        get(v14, v142, page)
        # break


if __name__ == '__main__':
    main()
    # print('5页总和:', all_sum)
