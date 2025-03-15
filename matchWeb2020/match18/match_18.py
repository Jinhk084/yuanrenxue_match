"""


"""
import base64
import time
from Crypto.Cipher import AES  # pip install pycryptodome
from Crypto.Util.Padding import pad

from matchWeb2020.config import BASE_URL, get_session, verify_answers

session = get_session()
all_sum = 0


def aes_encrypt(key, iv, plain_text):
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    ct_base64 = base64.b64encode(ct_bytes).decode('utf-8')
    return ct_base64


def main():
    global all_sum

    for page in range(1, 6):
        time_stamp = int(time.time())
        key = iv = hex(time_stamp)[2:] * 2
        plain_text = f'{page}|165m286,165m287,165m286,165d286,165u286' # 对鼠标轨迹校验不严格,直接写死
        cipher_text = aes_encrypt(key, iv, plain_text)
        resp = session.get(url=f'{BASE_URL}/match/18data',
                           params={'page': page,
                                   't': time_stamp,
                                   'v': cipher_text})
        resp_json = resp.json()
        print(page, resp_json)

        for item in resp_json['data']:
            all_sum += item['value']

    print('5页总和:', all_sum)
    verify_answers(session, all_sum, 18, '/api/answers')


if __name__ == '__main__':
    main()
