import numpy as np

from matchWeb2020.config import BASE_URL, get_session, compile_js, verify_answers

js_compiler = compile_js('match_05.js')
params = js_compiler.call('get_params')

session = get_session()
session.cookies.update({'RM4hZBv0dDon443M': params['RM4hZBv0dDon443M']})

allData = []
for page in range(1, 6):
    res = session.get(url=f"{BASE_URL}/api/match/5",
                      params={
                          'page': f'{page}',
                          'm': params['url_m'],
                          'f': params['url_m']
                      })

    resp_json = res.json()
    print(resp_json)
    for data in resp_json['data']:
        allData.append(data['value'])

max5_sum = sum(np.sort(allData)[-5:])  # 升序
print('前5名直播间热度和:', max5_sum)
verify_answers(session, max5_sum, 5)
