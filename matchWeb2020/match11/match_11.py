"""
    MainActivity.java 为 Unidbg 的代码
"""

import subprocess  # 直接用命令行调用能够避免环境的一些报错,也可以使用(jpype)
from matchWeb2020.config import BASE_URL, get_session, verify_answers


def run_jar_command(page: int) -> str:
    try:
        result = subprocess.run(
            ["java", "-jar", "unidbg-android.jar", str(page)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        return result.stdout.strip()  # 去除可能的换行符
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'调用Jar包执行失败 (Page={page}): {e.stderr}') from e
    except Exception as e:
        raise RuntimeError(f'调用Jar包时发生异常 (Page={page}): {str(e)}') from e


session = get_session()
all_sum = 0
for page in range(100):
    res = session.get(url=f"{BASE_URL}/api/match/11/query",
                      params={
                          'id': str(page),
                          'sign': run_jar_command(page)
                      })
    resp_json = res.json()
    print(page, resp_json)
    all_sum += resp_json['data']

print('总和:', all_sum)
verify_answers(session, all_sum, 11)
