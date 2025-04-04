from typing import Union

from requests import Session
import execjs

BASE_URL = "https://match.yuanrenxue.cn"
SESSION_ID = "7rrbw5fegtv4p3y8fs8aofk32nyh9ln4"


def get_session() -> Session:
    """
    创建并返回一个配置好的Session对象
    :return: 一个配置好的Session对象
    """
    session = Session()
    session.headers = {'User-Agent': 'yuanrenxue.project'}
    session.cookies.set('sessionid', SESSION_ID)

    return session


def compile_js(file_path: str):
    """
    编译JavaScript代码
    :param file_path: JavaScript代码文件的路径
    :return: 一个编译后的JavaScript程序对象
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        js_code = f.read()
    return execjs.compile(js_code)


def verify_answers(session: Session, answer: Union[str, int], num: Union[str, int], path=None) -> bool:
    """
    核对正确答案
    :param path:
    :param session: 用户的session对象
    :param answer: 题目的答案
    :param num: 题目的序号(根据不同的题目序号修改!!!)
    :return: True 或 False
    """
    answer_url = f'{BASE_URL}{path}' if path else f'{BASE_URL}/api/answer'
    response = session.get(url=answer_url,
                           params={
                               'answer': str(answer),
                               'id': str(num)
                           })
    resp_json = response.json()
    del resp_json['user']  # 账号名
    result = resp_json['status_code'] == '1'
    print(f'\033[92m第{num}题验证成功\033[0m' if result else f'\033[91m第{num}题验证失败\033[0m')
    return result
