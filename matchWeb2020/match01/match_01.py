from matchWeb2020.config import BASE_URL, get_session, compile_js, verify_answers

session = get_session()
js_compiler = compile_js('match_01.js')

all_sum = 0
for page in range(1, 6):
    res = session.get(url=f'{BASE_URL}/api/match/1',
                      params={
                          'page': str(page),
                          'm': js_compiler.call('get_m')
                      })
    # 求和
    for data in res.json()['data']:
        all_sum += data['value']
    print(page, res.json())

average_value = int(all_sum / 50)
print(f'5页平均值: {average_value}')
verify_answers(session, average_value, 1)
