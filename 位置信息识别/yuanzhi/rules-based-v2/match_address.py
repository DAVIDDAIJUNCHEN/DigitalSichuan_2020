from prepare_data.max_seg import PsegMax
import pandas as pd
import nltk

"""
定义常用的文件地址
"""
formal_address_files = "prepare_data/address_dicts_data/Standara_Address_Data_Of_A.csv"
dict_path = "prepare_data/address_dicts_data/all_address_dict.csv"
inputfile = "prepare_data/html2txt2clean/tokens_and_sentence.txt"
"""
"""


def get_formal_address():
    # 加载标准地址数据集
    dataframe = pd.read_csv(formal_address_files, sep='\t',
                            dtype={'locationx': str, 'locationy': str})

    dataframe = dataframe.fillna("")
    return dataframe


def get_tokens_and_sents(input_file):
    # 根据源文件构造tokens和sentence
    tokens = []
    sents = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            lines = line.split('$')
            tokens.append(lines[0].strip())
            sents.append(lines[1].strip())

    return tokens, sents


def find_poi_in_token(tokens, psg):
    # 找到tokens中所有的地名词语，并按他们所属类别返回一个词典
    poi_results = []
    for text in tokens:
        poi_dict = {'PROV': [], 'CIT': [], 'DIS': [], 'TOW': [], 'STR': []}
        words_psg = psg.max_biward_seg(text)
        for entity, tag in words_psg:
            if tag in poi_dict.keys():
                if entity not in poi_dict[tag]:
                    poi_dict[tag].append(entity)

        poi_results.append(poi_dict)

    return poi_results


def slim_data_by_domain(dataframe, poi_list, domain):
    # 根据给定的地名以及类别筛选数据
    dataframe_slim = pd.DataFrame()
    for poi_token in poi_list:
        if domain == 'street':
            dataframe_temp = dataframe[dataframe[domain] == poi_token]
        else:
            dataframe_temp = dataframe[dataframe[domain].str.contains(poi_token)]
        dataframe_slim = pd.concat([dataframe_slim, dataframe_temp], axis=0)

        # 索引去重
        dataframe_slim.drop_duplicates(keep='first', inplace=True)

    if len(poi_list) == 0:
        return dataframe
    else:
        return dataframe_slim


def dice_distance(reference, candidate):
    # 计算给定ref和can之间的相似度
    # 获取word字符级别的2元gram
    reference_list = list(nltk.ngrams(reference, 2, pad_left=True, pad_right=True, left_pad_symbol="!", right_pad_symbol="="))
    candidate_list = list(nltk.ngrams(candidate, 2, pad_left=True, pad_right=True, left_pad_symbol="!", right_pad_symbol="="))

    reference_lens = len(reference_list)
    candidate_lens = len(candidate_list)

    # 计算dice = (2 * (w1 and w2) ) / (w1.lens + w2.lens)
    score = len(set(reference_list).intersection(set(candidate_list))) * 2 / (reference_lens + candidate_lens)

    return score


def get_street_number(numbers, street, sentence):
    # 去除停用词
    sentence = sentence.replace('的', '')
    sentence = sentence.replace('吧', '')

    address = sentence.replace(street[0], '$')
    number_candidate = address.split('$')[-1].strip()

    max_score = 0
    best_number = ""
    for number in numbers:
        score = dice_distance(number_candidate, number)
        if score > max_score:
            max_score = score
            best_number = number

    return best_number


def save_to_csv(all_results):
    with open(r'results/500html_results.csv', 'w', encoding='utf-8') as f:
        f.write('filename,label' + '\n')
        for line in all_results:
            f.write(line)
            f.write('\n')


def get_address(dataframe, poi_results, sentences):
    # 'PROV': [], 'CIT': [], 'DIS': [], 'TOW': [], 'STR': []
    # 定义列表存放所有的识别结果
    all_results = []

    # 开始匹配每一个文件
    for i, poi_dict, sentence in zip(range(len(sentences)), poi_results, sentences):
        print("process " + str(i+1) + '.html')
        # 筛选数据，得到省~路的标准数据
        dataframe_street = slim_data_by_domain(dataframe, poi_dict['STR'], 'street')

        dataframe_town = slim_data_by_domain(dataframe_street, poi_dict['TOW'], 'township')
        if dataframe_town.shape[0] == 0:
            # 解决DIS和TOW存在重名的情况
            poi_dict['DIS'].extend(poi_dict['TOW'])
            dataframe_dis = slim_data_by_domain(dataframe_street, poi_dict['DIS'], 'district')
        else:
            dataframe_dis = slim_data_by_domain(dataframe_town, poi_dict['DIS'], 'district')

        if dataframe_dis.shape[0] == 0:
            # 解决CITY和DIS存在重名的情况
            poi_dict['CIT'].extend(poi_dict['DIS'])
            dataframe_city = slim_data_by_domain(dataframe_town, poi_dict['CIT'], 'city')
        else:
            dataframe_city = slim_data_by_domain(dataframe_dis, poi_dict['CIT'], 'city')

        if dataframe_city.shape[0] == 0:
            # 解决PROV和CITY存在重名的情况
            poi_dict['PROV'].extend(poi_dict['CIT'])
            dataframe_prov = slim_data_by_domain(dataframe_dis, poi_dict['PROV'], 'province')
        else:
            dataframe_prov = slim_data_by_domain(dataframe_city, poi_dict['PROV'], 'province')

        # 筛选数据，获取路号，然后做匹配
        if dataframe_prov.shape[0] > 1:
            if len(poi_dict['STR']) > 0:
                number = get_street_number(dataframe_prov['street_num'].values, poi_dict['STR'], sentence)
            elif len(poi_dict['TOW']) > 0:
                number = get_street_number(dataframe_prov['street_num'].values, poi_dict['TOW'], sentence)
            else:
                number = get_street_number(dataframe_prov['street_num'].values, poi_dict['DIS'], sentence)

            dataframe_all = dataframe_prov[dataframe_prov['street_num'] == number]

        else:
            number = get_street_number(dataframe_street['street_num'].values, poi_dict['STR'], sentence)
            dataframe_all = dataframe_prov[dataframe_prov['street_num'] == number]

        if dataframe_all.shape[0] > 0:
            results = str(i + 1) + '.html,' + "$".join(dataframe_all.values[0])
        else:
            results = str(i + 1) + '.html,'

        all_results.append(results)

    # 保存结果
    save_to_csv(all_results)

    return all_results


def debug():
    # 获取分词工具对象
    psg = PsegMax(dict_path)

    # 获取预处理文本的tokens及sentence
    # tokens, sentence = get_tokens_and_sents(inputfile)
    tokens = ["广西公园路园艺公园植物文竹福建10大片湖南安徽广东江西山上"]
    sentence = ["你见过吗？拍摄于美丽的公园路148号楼"]
    find_poi_in_token(tokens, psg)

    # 得到所有的地址识别结果
    poi_results = find_poi_in_token(tokens, psg)
    print(poi_results)

    # 获取标准地址数据集
    dataframe = get_formal_address()
    all_results = get_address(dataframe, poi_results, sentence)
    #
    print(all_results[0])


def main():
    # 获取双向最大距离分词工具
    psg = PsegMax(dict_path)

    # 获取待匹配文本的tokens及sentence
    # tokens表示在文章中出现过的所有与地名相关的词语
    # sentence表示包含XX路的句子文本
    tokens, sentence = get_tokens_and_sents(inputfile)

    # 得到所有的地址词语的识别结果, 每个城市类下对应城市名
    # 如：city: [], province: []
    poi_results = find_poi_in_token(tokens, psg)

    # 获取待匹配的标准地址数据集
    formal_address = get_formal_address()

    # 得到所有html文件的地址匹配结果
    all_results = get_address(formal_address, poi_results, sentence)


if __name__ == '__main__':
    # main()
    debug()
