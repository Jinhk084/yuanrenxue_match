import requests
import re
import execjs
from scrapy import Selector

envCode = '''
delete require;
window = {
    addEventListener: function (arg0, arg1, arg2) {},
};
document = {
    addEventListener: function (arg0, arg1, arg2) {
        if (arg0 === 'DOMContentLoaded') return arg1();
    },
    createElement: function (arg0) {
        switch (arg0) {
            case 'div':
                return {firstChild: {href: "https://www.python-spider.com/"}};
            default :
                return {};
        }
    }
};
let setTimeout = function () {};
function get_cookie() { return document.cookie; }
'''

session = requests.session()
session.cookies.update({'sessionid': 'nkv3d0eh3nr0daz6kjjmmj36zacjpw1s'})

#
resp_1 = session.get(url="https://www.python-spider.com/challenge/11")
html_js_code = re.findall(r'<script>(.*?)</script>', resp_1.text)[0]

# 本地获取cookie
Func = execjs.compile(envCode + html_js_code)
cookie = Func.call('get_cookie')
print('cookie:', cookie)

# 带上cookie再次请求
session.cookies.update({'__jsl_clearance': cookie.split('=')[1].replace(';Expires', '')})
resp_2 = session.get(url="https://www.python-spider.com/challenge/11")

# 解析
selector = Selector(resp_2)
datas = selector.xpath("//div['page-box layui-row']//td['info']/text()").getall()
datas = [int(i.strip()) for i in datas]
print('总和:', sum(datas))
