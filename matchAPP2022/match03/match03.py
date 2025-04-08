import time
import jpype

from matchAPP2022.config import get_session, BASE_URL, verify_answers

# 启动Java虚拟机
jpype.startJVM(
    jpype.getDefaultJVMPath(),
    classpath=['match03.jar']
)
JavaClass = jpype.JClass('com.yuanrenxue.app2022.match03.MainActivity')

session = get_session()
page100Sum = 0
for page in range(1, 101):
    timeStamp = int(time.time()) * 1000

    #
    m = str(JavaClass.crypto(f'{page:03d}{timeStamp}', str(timeStamp)))

    #
    resp = session.post(url=f'{BASE_URL}/app3',
                        data={
                            'page': str(page),
                            'm': m,
                            'token': '',
                        })
    resp_json = resp.json()
    print(page, resp_json)
    for data in resp_json['data']:
        page100Sum += int(data['value'].strip())

jpype.shutdownJVM()
# print('100页总和:', page100Sum)
verify_answers(session, page100Sum, 3)
