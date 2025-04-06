import time
import subprocess

from matchAPP2022.config import get_session, BASE_URL, verify_answers

session = get_session()
page100Sum = 0
for page in range(1, 101):
    timeStamp = int(time.time())
    plain_text = f'{page}:{timeStamp}'

    #
    result = subprocess.run(
        ['java', '-jar', 'unidbg-android.jar', plain_text],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    sign = result.stdout.strip()

    #
    resp = session.post(url=f'{BASE_URL}/app2',
                        params={
                            'token': '',  # 可以不传
                        },
                        data={
                            'page': str(page),
                            'ts': str(timeStamp),
                            'sign': sign,
                        })
    resp_json = resp.json()
    print(page, resp_json)
    for data in resp_json['data']:
        page100Sum += int(data['value'].strip())

# print('100页总和:', page100Sum)
verify_answers(session, page100Sum, 2)
