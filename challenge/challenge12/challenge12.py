"""
题目是 "静态css加密", 所示只需要构建一个字体映射表就行了
"""

import requests

font_map = {
    '&#xf712': '0',
    '&#xe458': '1',
    '&#xf375': '2',
    '&#xf80c': '3',
    '&#xf12f': '4',
    '&#xee4a': '5',
    '&#xf295': '6',
    '&#xe449': '7',
    '&#xf0d6': '8',
    '&#xe44d': '9',
}

headers = {'Cookie': "sessionid=nkv3d0eh3nr0daz6kjjmmj36zacjpw1s;"}

all_sum = 0
for page in range(1, 101):

    response = requests.post(url="https://www.python-spider.com/api/challenge12",
                             headers=headers,
                             data={'page': page})

    items = response.json()['data']
    items = [i['value'].split(' ')[:-1] for i in items]

    nums = []
    for data_list in items:
        numbers = []
        for data in data_list:
            numbers.append(font_map[data])
        nums.append(''.join(numbers))
    nums = [int(i) for i in nums]

    all_sum += sum(nums)
    print(f'page({page}):', nums)

print('100页总和:', all_sum)
