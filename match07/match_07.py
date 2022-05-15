import requests
# https://fontcreator.com.cn/download/
from lxml import etree  # pip install lxml
from fontTools.ttLib import TTFont  # pip install fonttools
import base64


def get_data_font(page):
    headers = {
        "user-agent": "yuanrenxue.project",
        # "cookies": "sessionid=zsl8th192izmvaq7nicphmnii4vr18nj"
    }
    url = "https://match.yuanrenxue.com/api/match/7"
    params = {
        "page": str(page)
    }
    res = requests.get(url, headers=headers, params=params)
    res_json = res.json()

    # 网站加密的数据
    data_list = res_json['data']

    # 获取字体加密数据并保存
    font_file = base64.b64decode(res_json['woff'])
    with open('match_07.ttf', 'wb')as file:
        file.write(font_file)

    # 转换格式: ttf --> xml
    font_obj = TTFont('match_07.ttf')
    font_obj.saveXML('match_07.xml')

    return data_list


def parse_data(data_list, page):
    # 构造on的映射字典
    xml = etree.parse('match_07.xml')
    uni_to_on = dict()
    for obj in xml.xpath('//TTGlyph'):
        on = obj.xpath('.//pt/@on')
        value = ''.join(on)
        key = obj.xpath('./@name')[0]
        uni_to_on[key] = value
    # print(uni_to_on)

    # 修改机密数字操作
    yyq = 1
    for data in data_list:
        info = data['value'].split(' ')[:-1]  # ['&#xe691', '&#xb261', '&#xe691', '&#xc931']
        info = [i.replace('&#x', 'uni') for i in info]  # 替换: &#x --> uni
        data_end = ['0'] * len(info)  # 创建空列表
        for index in range(len(info)):
            data_end[index] = on_to_num[uni_to_on[info[index]]]
        all_data.append(''.join(data_end))

        name_data.append(name[yyq + (page - 1) * 10])
        yyq += 1


if __name__ == '__main__':
    name = ['极镀ギ紬荕', '爷灬霸气傀儡', '梦战苍穹', '傲世哥', 'мaη肆風聲', '一刀メ隔世', '横刀メ绝杀', 'Q不死你R死你', '魔帝殤邪', '封刀不再战', '倾城孤狼', '戎马江湖',
            '狂得像风', '影之哀伤', '謸氕づ独尊', '傲视狂杀', '追风之梦', '枭雄在世', '傲视之巅', '黑夜刺客', '占你心为王', '爷来取你狗命', '御风踏血', '凫矢暮城', '孤影メ残刀',
            '野区霸王', '噬血啸月', '风逝无迹', '帅的睡不着', '血色杀戮者', '冷视天下', '帅出新高度', '風狆瑬蒗', '灵魂禁锢', 'ヤ地狱篮枫ゞ', '溅血メ破天', '剑尊メ杀戮',
            '塞外う飛龍', '哥‘K纯帅', '逆風祈雨', '恣意踏江山', '望断、天涯路', '地獄惡灵', '疯狂メ孽杀', '寂月灭影', '骚年霸称帝王', '狂杀メ无赦', '死灵的哀伤', '撩妹界扛把子',
            '霸刀☆藐视天下', '潇洒又能打', '狂卩龙灬巅丷峰', '羁旅天涯.', '南宫沐风', '风恋绝尘', '剑下孤魂', '一蓑烟雨', '领域★倾战', '威龙丶断魂神狙', '辉煌战绩', '屎来运赚',
            '伱、Bu够档次', '九音引魂箫', '骨子里的傲气', '霸海断长空', '没枪也很狂', '死魂★之灵']
    on_to_num = {
        '1110101001001010110101010100101011111': '5',
        '101010101101010001010101101010101010010010010101001000010': '8',
        '10101010100001010111010101101010010101000': '6',
        '10100100100101010010010010': '0',
        '10010101001110101011010101010101000100100': '9',
        '1111111': '7',
        '100110101001010101011110101000': '2',
        '10101100101000111100010101011010100101010100': '3',
        '1001101111': '1',
        '111111111111111': '4'
    }
    all_data = []
    name_data = []

    for page in range(1, 6):
        # 获取网页返回的数据和动态的字体文件
        data_list = get_data_font(page)
        # print(data_list)
        parse_data(data_list, page)

    # max_index = all_data.index(max(all_data))
    # print(name_data[max_index])
