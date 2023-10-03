import requests
import jpype  # pip install JPype1
import time
from loguru import logger

jpype.startJVM()  # 启动JVM
# 需要 javac Match01.java 生成 Match01.class和Sign.class才可以
Match01 = jpype.JClass('Match01')  # 加载Java类

page100Sum = 0  # 100页之和

for page in range(1, 101):
    # # 获取时间戳
    # respJson = requests.get('https://appmatch.yuanrenxue.cn/time', params={
    #     'token': '',
    # }).json()
    #
    # timeStamp = respJson['time']
    # logger.info(f'page--> {page} | timeStamp--> {timeStamp}')

    timeStamp = int(time.time())

    sign = Match01.getSign(page, timeStamp)  # 调用Java代码
    logger.info(f'page--> {page} | sign--> {sign}')

    # 请求数据
    response = requests.post(url='https://appmatch.yuanrenxue.cn/app1',
                             headers={
                                 'Host': 'appmatch.yuanrenxue.cn',
                                 'accept-language': 'zh-CN,zh;q=0.8',
                                 'user-agent': 'Mozilla/5.0 (Linux; U; Android 10; zh-cn; Pixel 4 XL Build/QQ3A.200805.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
                                 'content-type': 'application/x-www-form-urlencoded',
                                 'cache-control': 'no-cache',
                             },
                             data={
                                 'page': str(page),
                                 'sign': str(sign),
                                 't': str(timeStamp),
                                 'token': '',  # 省略
                             })

    logger.info(response.json())
    onePageSum = 0
    for data in response.json()['data']:
        onePageSum += int(data['value'].strip())
    page100Sum += onePageSum

jpype.shutdownJVM()  # 关闭JVM

logger.success(f'100页之和: {page100Sum}')
