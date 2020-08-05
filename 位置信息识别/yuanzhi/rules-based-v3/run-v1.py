from tools.tokenizer import PsegMax
import pandas as pd
import nltk
import math
import re
import time

"""
定义常用的文件地址
"""
formal_address_files = "data/standard_address_dataset.csv"
dict_path = "dicts/ALL.dict"
inputfile = "data/tokens_and_sentences/tokens_and_sentence.txt"
outputfile = "results/0804-5_results.csv"
patternfile = "data/regex/pattern.re"
"""
"""


def get_formal_address():
    # 加载标准地址数据集
    dataframe = pd.read_csv(formal_address_files, sep='\t',
                            dtype={'locationx': str, 'locationy': str})

    dataframe = dataframe.fillna("")
    return dataframe


def get_re_pattern():
    patterns = {}
    with open(patternfile, 'r', encoding='utf-8') as f:
        for line in f:
            lst = line.split()
            patterns[lst[-1]] = lst[0]

    return patterns


patterns = get_re_pattern()


def sort_strings_with_emb_numbers2(alist):
    # 对字符数组排序
    def emb_numbers(s):
        re_digits = re.compile(r'(\d+)')
        pieces = re_digits.split(s)
        pieces[1::2] = map(int, pieces[1::2])
        pieces.extend([-1, -1, -1])
        pieces[2:3] = pieces[3:2]
        pieces[3:4] = pieces[4:3]
        return pieces

    return sorted(alist, key=emb_numbers)


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
        poi_dict = {'PRO': [], 'CIT': [], 'DIS': [], 'TOW': [], 'STR': []}
        words_psg = psg.max_biward_seg(text)
        for entity, tag in words_psg:
            if tag in poi_dict.keys():
                if entity not in poi_dict[tag]:
                    poi_dict[tag].append(entity)

        poi_results.append(poi_dict)

    return poi_results


def slim_data_by_domain(dataframe, poi_list, domain):
    # 根据给定的地名以及类别筛选数据
    # 如果poi_list中数据为空，则返回原df
    if len(poi_list) == 0:
        return dataframe

    dataframe_slim = pd.DataFrame()
    for poi_token in poi_list:
        if domain == 'street' or domain == 'township':
            dataframe_temp = dataframe[dataframe[domain] == poi_token]
        else:
            dataframe_temp = dataframe[dataframe[domain].str.contains(poi_token)]

        dataframe_slim = pd.concat([dataframe_slim, dataframe_temp], axis=0)

        # 索引去重
        dataframe_slim.drop_duplicates(keep='first', inplace=True)

    return dataframe_slim


def dice_distance(reference, candidate):
    # 计算给定ref和can之间的相似度
    # 获取word字符级别的2元gram
    reference_list = list(
        nltk.ngrams(reference, 2, pad_left=True, pad_right=True, left_pad_symbol="!", right_pad_symbol="="))
    candidate_list = list(
        nltk.ngrams(candidate, 2, pad_left=True, pad_right=True, left_pad_symbol="!", right_pad_symbol="="))

    reference_lens = len(reference_list)
    candidate_lens = len(candidate_list)

    # 计算dice = (2 * (w1 and w2) ) / (w1.lens + w2.lens)
    score = len(set(reference_list).intersection(set(candidate_list))) * 2 / (
            reference_lens + candidate_lens)

    return score


def left_or_right(candidates, size, k, width=5, method='char'):
    width_left = width
    width_right = width
    if k < width:
        width_left = k
    if (size-1)-k < width:
        width_right = (size-1)-k

    if method == 'char':
        if size == 1:
            return candidates[0]
        if k == 0:
            return candidates[k+1]
        elif k == size-1:
            return candidates[k-1]
        else:
            score_left = dice_distance(candidates[k-1], candidates[k])
            score_right = dice_distance(candidates[k+1], candidates[k])
            if score_left > score_right:
                return candidates[k-1]
            else:
                return candidates[k+1]
    elif method == 'nums_one':
        hash_flag = {}

        nums_ref = re.findall(r'\d+', candidates[k])
        for j in range(k-width_left, k+width_right):
            nums_cand = re.findall(r'\d+', candidates[j])
            if len(nums_cand) == 0:
                continue
            elif len(nums_cand) == 2:
                if int(nums_ref[0])-int(nums_cand[0]) in hash_flag.keys():
                    continue
                else:
                    hash_flag[int(nums_ref[0])-int(nums_cand[0])] = candidates[j]
            else:
                hash_flag[int(nums_ref[0])-int(nums_cand[0])] = candidates[j]

        for m in range(2, 40, 2):
            if -m in hash_flag.keys():
                return hash_flag[-m]
            elif m in hash_flag.keys():
                return hash_flag[m]

        dis = 999999
        key_key = 99999
        for key in hash_flag.keys():
            if 0 < abs(key) < dis:
                dis = abs(key)
                key_key = key

        if key_key < 99999:
            return hash_flag[key_key]

        if size == 1:
            return candidates[0]
        if k-1 >= 0:
            return candidates[k-1]
        elif k+1 <= size:
            return candidates[k+1]
        else:
            return "NP"


def find_best_num(candidates, ref_sents, charnums):
    size = len(candidates)

    flag = -1
    for k in range(size):
        if candidates[k] == ref_sents:
            flag = k

    if charnums == "1":
        nums = re.findall(r'[a-zA-Z\d]+', ref_sents)
        nums_char = re.findall(r'[a-zA-Z]+', nums[0])
        if len(nums_char) > 0:
            best_number = left_or_right(candidates, size, flag)
        else:
            best_number = left_or_right(candidates, size, flag, method='nums_one', width=5)
    else:
        best_number = left_or_right(candidates, size, flag)

    return best_number


def get_street_number(candidates, reference, method='precise'):
    # 精确匹配+模糊匹配 正则
    # NP: not precise
    best_number = ""
    likely_number = ""

    ref_pattern = r"[a-zA-Z\d]+[#号栋楼幢座巷弄]"
    for pats in patterns.keys():
        temp_number = re.findall(pats.replace('\n', ''), reference)
        if len(temp_number) > 0 and len(temp_number[0]) > len(likely_number):
            likely_number = temp_number[0]
            ref_pattern = pats

    if likely_number == "":
        likely_number = "NP"

    if method == 'precise':
        candidates = sorted(candidates, key=lambda i: len(i))

        if likely_number in list(candidates):
            return likely_number
        else:
            return "NP"
    else:
        # 模糊匹配
        ref_sents = likely_number

        # 将匹配出来的串放进去，一起排序
        candidates = list(candidates)
        candidates.append(ref_sents)
        candidates = sort_strings_with_emb_numbers2(candidates)

        if ref_sents == "NP":
            candidates.remove(ref_sents)
            max_score = 0.0
            for num in candidates:
                if dice_distance(num, reference) >= max_score:
                    max_score = dice_distance(num, reference)
                    best_number = num
        else:
            best_number = find_best_num(candidates, ref_sents, patterns[ref_pattern])

        return best_number


def from_province_to_street(df_first, poi_dict, sentence):
    # 匹配从路到省的信息
    df_temp = pd.DataFrame(df_first, columns=['province', 'city', 'district', 'township', 'street'])
    if df_temp.shape[0] == 1:
        # 如果shape为1，则表明包含该路号的数据仅一条，可以直接输出
        number = get_street_number(df_first['street_num'].values, sentence)
        df_second = df_first

        return number, df_second
    else:
        # 第二次缩减数据 解决省市区之间可能的重名问题，
        # 吉林(省)和吉林(市)拍了拍旁边朝阳(区)和朝阳(县)老弟，讨论去海南(省)还是海南(州)旅游
        poi_dict['PRO'].extend(poi_dict['CIT'])
        poi_dict['PRO'].extend(poi_dict['DIS'])
        poi_dict['CIT'].extend(poi_dict['DIS'])

        # -->开始逐级精确匹配
        # +街道/镇
        df_tow = slim_data_by_domain(df_first, poi_dict['TOW'], 'township')
        number = get_street_number(df_tow['street_num'].values, sentence)
        if number != "NP":
            df_second = df_tow
        else:
            # +区/县
            df_dis = slim_data_by_domain(df_first, poi_dict['DIS'], 'district')
            number = get_street_number(df_dis['street_num'].values, sentence)
            if number != "NP":
                df_second = df_dis
            else:
                # +市
                df_cit = slim_data_by_domain(df_first, poi_dict['CIT'], 'city')
                number = get_street_number(df_cit['street_num'].values, sentence)
                if number != "NP":
                    df_second = df_cit
                else:
                    # +省
                    df_pro = slim_data_by_domain(df_first, poi_dict['PRO'], 'province')
                    number = get_street_number(df_pro['street_num'].values, sentence)
                    if number != "NP":
                        df_second = df_pro
                    else:
                        # 开始大面积的精确匹配
                        # 合并数据并索引去重
                        number = get_street_number(df_first['street_num'].values, sentence)
                        if number != "NP":
                            df_second = df_first
                        else:
                            # 开始模糊匹配
                            df_tow = slim_data_by_domain(df_first, poi_dict['TOW'], 'township')
                            df_dis = slim_data_by_domain(df_first, poi_dict['DIS'], 'district')
                            df_cit = slim_data_by_domain(df_first, poi_dict['CIT'], 'city')
                            df_pro = slim_data_by_domain(df_first, poi_dict['PRO'], 'province')

                            if df_tow.shape[0] > 0: df_second = df_tow
                            elif df_dis.shape[0] > 0: df_second = df_dis
                            elif df_cit.shape[0] > 0: df_second = df_cit
                            elif df_pro.shape[0] > 0: df_second = df_pro
                            else: df_second = df_first

        if number == "NP":
            return number, df_second
        else:
            number2 = ""
            for num in sorted(df_tow['street_num'].values, key=lambda i: len(i), reverse=True):
                if num in sentence:
                    number2 = num
                    break

            if len(number2) > len(number):
                return number2, df_second
            else:
                return number, df_second


def from_street_num(df_second, number, sentence, method='precise'):
    # 获取最好的路号
    if method == 'likely':
        # 未能精准匹配，眼睛一转，看来我们之中混入了刺客。找出它，干掉它
        # 首先考虑地址名词的干扰情况，再次进行精准匹配
        number = get_street_number(df_second['street_num'].values, sentence, method='likely')

        best_number = ""
        max_score = 0.0
        for num in list(df_second['street_num'].values):
            if dice_distance(num, sentence) >= max_score:
                max_score = dice_distance(num, sentence)
                best_number = num

        if len(best_number) >= 9:
            # 如果标准地址太长，则不考虑奇偶规则
            df_second = df_second[df_second['street_num'] == best_number]
        elif number != "NP":
            # 喜大普奔, 精准匹配在这里成功了
            # 实行精准匹配抓捕计划
            df_second = df_second[df_second['street_num'] == number]
        else:
            df_second = df_second[df_second['street_num'] == best_number]
    else:
        # 第一次就OK啦，爱死你了
        # 跟我走吧，精准匹配
        df_second = df_second[df_second['street_num'] == number]

    return number, df_second


def save_to_csv(all_results):
    with open(outputfile, 'a+', encoding='utf-8') as f:
        # f.write('filename,label' + '\n')
        for line in all_results:
            f.write(line)
            f.write('\n')


def get_address_copy(dataframe, poi_results, sentences, method='debug'):
    # poi_dict = 'PRO': [], 'CIT': [], 'DIS': [], 'TOW': [], 'STR': []
    # 开始匹配每一个文件, 匹配分两步：先匹配省到路名，第二步求路号
    all_results = []

    for i, poi_dict, sentence in zip(range(len(sentences)), poi_results, sentences):
        if len(poi_dict['STR']) > 0:
            sentence = sentence.replace(poi_dict['STR'][0], "", 1)
            if len(poi_dict['TOW']) > 0:
                sentence = sentence.replace(poi_dict['TOW'][0], '', 1)
        elif len(poi_dict['TOW']) > 0:
            sentence = sentence.replace(poi_dict['TOW'][0], "", 1)
        else:
            pass

        # 筛选数据，得到省~路的标准数据
        print("process " + str(i + 1) + '.html')
        if len(poi_dict['STR']) > 0:
            df_first = slim_data_by_domain(dataframe, poi_dict['STR'], 'street')
        elif len(poi_dict['TOW']) > 0:
            df_first = slim_data_by_domain(dataframe, poi_dict['TOW'], 'township')
        else:
            df_first = slim_data_by_domain(dataframe, poi_dict['DIS'], 'district')

        # 获取从省到路的地址信息
        number, df_second = from_province_to_street(df_first, poi_dict, sentence)

        # 匹配路号
        if number != "NP":
            # 获取最终的路号信息，及唯一的地址
            number, df_last = from_street_num(df_second, number, sentence, method='precise')
        else:
            number, df_last = from_street_num(df_second, number, sentence, method='likely')
            # df_last = pd.DataFrame()

        # 快保存结果，提交看看得分
        if df_last.shape[0] > 0:
            # 如果有多条，我要开始随机取了，我也很无奈呀 :(
            results = str(i + 1) + '.html,' + "$".join(df_last.values[0])
        else:
            # 大概率是没可能跳转到这步了，但为了逻辑的完整性还是留着吧
            results = str(i + 1) + '.html,'

        all_results.append(results)

        # 看看需不需要测试一下是否有BUG，不然一次10000条，要鸡丝人噢
        if method == 'debug':
            print(all_results)
        elif (i + 1) % 1000 == 0:
            # 出1000条就保存一次吧，万一电脑呆住了，那就很尴尬
            # 当然真呆住了，也拿Ta没办法 /狗头/狗头
            save_to_csv(all_results)
            all_results = []

    print("Done")


def main():
    # 获取双向最大距离分词工具
    psg = PsegMax(dict_path)

    # 获取待匹配文本的tokens及sentence
    # tokens表示在文章中出现过的所有与地名相关的词语
    # sentence表示包含XX路XX号(栋、楼)的句子文本
    tokens, sentence = get_tokens_and_sents(inputfile)

    # 得到所有的地址词语的识别结果, 每个城市类下对应城市名
    # 如：city: [], province: []
    poi_results = find_poi_in_token(tokens, psg)

    # 获取待匹配的标准地址数据集
    formal_address = get_formal_address()

    # 得到所有html文件的地址匹配结果
    get_address_copy(formal_address, poi_results, sentence, method='input')


def debug():
    # 获取分词工具对象
    psg = PsegMax(dict_path)

    # 获取预处理文本的tokens及sentence
    # tokens, sentence = get_tokens_and_sents(inputfile)
    # 安徽省	合肥市	包河区		莲花路	3269号
    tokens = []
    sentence = []

    # $”湖北省 古楼路 厦门 福建$购票地点：古楼路169号
    tokens.append("环城镇 林业巷 河北省")
    sentence.append("位于林业巷5号的小鹏汽车智能网联科技产业园就已完成奠基仪式")

    # 得到所有的地址识别结果
    poi_results = find_poi_in_token(tokens, psg)
    print(poi_results)

    # 获取标准地址数据集
    dataframe = get_formal_address()

    # method=debug, input
    get_address_copy(dataframe, poi_results, sentence)


if __name__ == '__main__':
    # main()
    t1 = time.time()
    # debug()
    main()
    print(time.time()-t1)


