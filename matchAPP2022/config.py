from typing import Union
from requests import Session

BASE_URL = "https://appmatch.yuanrenxue.cn"
TOKEN = "gMjm8b0yq8HE+diRslxNQ52cZZ/AFd/BmzRJoAYS8k0TwbOYB50DfniVJjVCrYPv"


def get_session() -> Session:
    """
    创建并返回一个配置好的Session对象
    :return: 一个配置好的Session对象
    """
    session = Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; zh-cn; Pixel 4 XL Build/QQ3A.200805.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/x-www-form-urlencoded; application/x-www-form-urlencoded; charset=utf-8',
        'accept-language': 'zh-CN,zh;q=0.8',
        'cache-control': 'no-cache',
    }
    return session


def verify_answers(session: Session, answer: Union[str, int], num: Union[str, int]) -> bool:
    """
    核对正确答案
    :param session: 用户的session对象
    :param answer: 题目的答案
    :param num: 题目的序号(根据不同的题目序号修改!!!)
    :return: True 或 False
    """
    resp = session.post(url=f'{BASE_URL}/check',
                        params={'token': TOKEN},
                        data={
                            'id': str(num),
                            'answer': str(answer),
                            'token': TOKEN,
                        })
    resp_json = resp.json()
    result = resp_json['status_code'] == '1'
    print(f'\033[92m第{num}题验证成功\033[0m' if result else f'\033[91m第{num}题验证失败\033[0m')
    return result
