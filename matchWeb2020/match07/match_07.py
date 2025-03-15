import base64
import os
from io import BytesIO
import xml.etree.ElementTree as Et
from fontTools.ttLib import TTFont  # pip install fonttools
from matchWeb2020.config import BASE_URL, get_session, verify_answers
import tempfile

# 字形到数字的映射
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

# 用户名字列表
name = ['极镀ギ紬荕', '爷灬霸气傀儡', '梦战苍穹', '傲世哥', 'мaη肆風聲', '一刀メ隔世', '横刀メ绝杀', 'Q不死你R死你',
        '魔帝殤邪', '封刀不再战', '倾城孤狼', '戎马江湖',
        '狂得像风', '影之哀伤', '謸氕づ独尊', '傲视狂杀', '追风之梦', '枭雄在世', '傲视之巅', '黑夜刺客', '占你心为王',
        '爷来取你狗命', '御风踏血', '凫矢暮城', '孤影メ残刀',
        '野区霸王', '噬血啸月', '风逝无迹', '帅的睡不着', '血色杀戮者', '冷视天下', '帅出新高度', '風狆瑬蒗',
        '灵魂禁锢', 'ヤ地狱篮枫ゞ', '溅血メ破天', '剑尊メ杀戮',
        '塞外う飛龍', '哥‘K纯帅', '逆風祈雨', '恣意踏江山', '望断、天涯路', '地獄惡灵', '疯狂メ孽杀', '寂月灭影',
        '骚年霸称帝王', '狂杀メ无赦', '死灵的哀伤', '撩妹界扛把子',
        '霸刀☆藐视天下', '潇洒又能打', '狂卩龙灬巅丷峰', '羁旅天涯.', '南宫沐风', '风恋绝尘', '剑下孤魂', '一蓑烟雨',
        '领域★倾战', '威龙丶断魂神狙', '辉煌战绩', '屎来运赚',
        '伱、Bu够档次', '九音引魂箫', '骨子里的傲气', '霸海断长空', '没枪也很狂', '死魂★之灵']

session = get_session()
name_list = []  # 存储所有名字
page_list = []  # 存储所有页面的值


def decrypt_font(woff_b64):
    # Base64解码
    woff_data = base64.b64decode(woff_b64)

    # 解析字体并保存
    font = TTFont(BytesIO(woff_data))
    font.saveXML('font.xml')


def get_on_sequence(woff_b64: str) -> dict:
    # 解码 Base64 字符串
    woff_data = base64.b64decode(woff_b64)

    # 将 WOFF 数据保存为临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.woff') as temp_file:
        temp_file.write(woff_data)
        temp_file_path = temp_file.name

    # 使用 fontTools 将 WOFF 转换为 TTX（XML 格式）
    ttx_path = temp_file_path.replace('.woff', '.ttx')
    font = TTFont(temp_file_path)
    font.saveXML(ttx_path)

    # 解析 TTX 文件
    tree = Et.parse(ttx_path)
    root = tree.getroot()
    cmap = {}
    for glyph in root.findall('.//TTGlyph'):
        name = glyph.get('name')
        if name.startswith('uni'):
            value = ''.join([pt.get('on') for pt in glyph.findall('.//pt')])
            key = glyph.get('name')
            cmap[key] = value

    # 删除临时文件
    os.remove(temp_file_path)
    os.remove(ttx_path)

    return cmap


def get_ong_page(page):
    resp = session.get(url=f'{BASE_URL}/api/match/7',
                       params={'page': f'{page}'})
    resp_json = resp.json()
    return resp_json['woff'], resp_json['data']


def parse_resp_data(datas, font_map, page):
    yyq = 1
    page_value = []
    for data in datas:
        d_str = data['value'].replace('&#x', 'uni')
        data_str = d_str.split(' ')[:-1]
        for i in range(len(data_str)):
            data_str[i] = on_to_num[font_map[data_str[i]]]
        page_value.append(int(''.join(data_str)))

        # 召唤师名字偏移操作
        name_list.append(name[yyq + (page - 1) * 10])
        yyq += 1

    return page_value


def main():
    for page in range(1, 6):
        # 获取 WOFF 字体文件和数据
        woff_b64, datas = get_ong_page(page)
        # decrypt_font(woff_b64)

        # 解析 WOFF 字体文件
        font_map = get_on_sequence(woff_b64)

        # 解析响应数据
        page_value = parse_resp_data(datas, font_map, page)
        print(page, page_value)
        page_list.extend(page_value)

    # 获取5页数据中最大的索引
    max_index = page_list.index(max(page_list))

    # 获取最大索引对应的名字
    max_value_name = name_list[max_index]
    print(f'胜点最高的召唤师: {max_value_name}')
    # 验证答案
    verify_answers(session, max_value_name, 7)


if __name__ == '__main__':
    main()
