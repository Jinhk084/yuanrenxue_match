import time
from matchWeb2020.config import BASE_URL, get_session, compile_js, verify_answers

session = get_session()
js_compiler = compile_js('match_06.js')

all_sum = 0
for page in range(1, 6):
    # 构造请求参数
    t = int(time.time()) * 1000
    # 请求数据
    res = session.get(url=f'{BASE_URL}/api/match/6',
                      params={
                          'page': f'{page}',
                          'm': js_compiler.call('get_params', t, 1),
                          'q': f'1-{t}|'
                      })
    resp_json = res.json()
    print(resp_json)
    for data in resp_json['data']:
        all_sum += data['value'] + data['value'] * 23

print(f'总金额: {all_sum}')
verify_answers(session, all_sum, 6)
