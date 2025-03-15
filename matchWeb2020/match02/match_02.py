from matchWeb2020.config import BASE_URL, get_session, compile_js, verify_answers

session = get_session()
js_compiler = compile_js('match_02.js')

all_sum = 0
for page in range(1, 6):
    session.cookies.update({'m': js_compiler.call('get_m')})
    res = session.get(url=f'{BASE_URL}/api/match/2',
                      params={
                          'page': str(page),
                      })
    print(page, res.json())
    for data in res.json()['data']:
        all_sum += data['value']

print(f'5页总和: {all_sum}')
verify_answers(session, all_sum, 2)
