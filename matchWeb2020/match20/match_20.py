import hashlib
import time
from matchWeb2020.config import BASE_URL, get_session, compile_js, verify_answers

session = get_session()


def md5_encrypt(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()


salt = "D#uqGdcw41pWeNXm"
all_sum = 0
for page in range(1, 6):
    time_stamp = int(time.time()) * 1000
    plain_text = f'{page}|{time_stamp}{salt}'
    res = session.get(url=f'{BASE_URL}/api/match/20',
                      params={
                          'page': f'{page}',
                          'sign': md5_encrypt(plain_text),
                          't': str(time_stamp)
                      })
    resp_json = res.json()
    print(resp_json)
    for data in resp_json['data']:
        all_sum += data['value']

print('5页总和:', all_sum)
verify_answers(session, all_sum, 20)
