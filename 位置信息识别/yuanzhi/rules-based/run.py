import pandas as pd
import jieba
import numpy as np
import os


class AddressDict(object):
    def __init__(self, input_file):
        """
        Args:
            input_file: Standara_Address_Data_Of_A.csv
            province	city	district	township	street	street_num	locationx	    locationy
            安徽省	   阜阳市	界首市	    西城街道	    界光路	 561号	    115.36780966    33.27176266
            1:
        """
        self.input_file = input_file
        self.address_list = pd.read_csv(input_file, sep='\t', dtype={'locationx': str, 'locationy': str})
        self.origin_address_list = self.address_list.copy().fillna('')

    def formal_missing_token(self, dataframe):
        """
        Args:
            dataframe: 输入的标准地址数据集
        formal key-words: 只处理street, street_num和township这三个字段, 因为只有这三个字段存在缺失值
        formal rules:
            1:仅street_num缺失
            2:
            3:
        Returns: 处理缺失值后的标准地址数据集
        """

        # fill null for township
        index_township_null = dataframe[dataframe['township'].isnull() == True].index
        dataframe.loc[index_township_null, 'township'] = dataframe.loc[index_township_null, 'district']

        # both street_num and street are all null
        index_two_null = dataframe[
            (dataframe['street'].isnull() == True) & (dataframe['street_num'].isnull() == True)].index
        dataframe.loc[index_two_null, 'street'] = dataframe.loc[index_two_null, 'township']
        dataframe.loc[index_two_null, 'street_num'] = ''

        # only street_num is null
        index_one_null = dataframe[dataframe['street_num'].isnull() == True].index
        dataframe.loc[index_one_null, 'street_num'] = ''

        # only street is null
        index_one_next_null = dataframe[dataframe['street'].isnull() == True].index
        dataframe.loc[index_one_next_null, 'street'] = dataframe.loc[index_one_next_null, 'township']

        return dataframe

    def slim_by_domain(self, dataframe, domain, token):
        if domain not in dataframe.columns:
            assert "Not Found columns: {}".format(domain)
            return dataframe

        # 如果domain是[district, city, province], 则使用模糊匹配筛选
        # 因为可能存在广州、广州市这两种情况，不能够使用精准匹配
        if domain == 'district' or domain == 'city' or domain == 'province':
            return dataframe[dataframe[domain].str.contains(token)]
        else:
            return dataframe[dataframe[domain] == token]

    def slim_data(self, address_list, tokens):
        # 根据street筛选数据
        slim_by_street_df = pd.DataFrame(columns=address_list.columns)

        for token in tokens:
            if token in list(address_list['street']):
                slim_by_street_df = pd.concat(
                    [slim_by_street_df, self.slim_by_domain(address_list, 'street', token)])

        # 如果上面得出的数据里，township列不唯一，则继续根据street+township 筛选数据
        slim_by_townshaip_df = slim_by_street_df

        if len(slim_by_street_df['township'].value_counts()) > 1:
            slim_by_townshaip_df = pd.DataFrame(columns=address_list.columns)
            for token in tokens:
                if token in list(slim_by_street_df['township']):
                    slim_by_townshaip_df = pd.concat(
                        [slim_by_townshaip_df, self.slim_by_domain(slim_by_street_df, 'township', token)], axis=0)

        # 如果上面得出的数据里，district列不唯一，则继续根据street+district 筛选数据
        slim_by_district_df = slim_by_street_df
        if len(slim_by_street_df['district'].value_counts()) > 1:
            slim_by_district_df = pd.DataFrame(columns=address_list.columns)
            for token in tokens:
                if len(token) > 1 and token in list(slim_by_street_df['district']):
                    slim_by_district_df = pd.concat(
                        [slim_by_district_df, self.slim_by_domain(slim_by_street_df, 'district', token)], axis=0)

        slim_by_townshaip_df = pd.concat([slim_by_townshaip_df, slim_by_district_df], axis=0)

        # 根据district+township+street判断
        slim_by_district_df = slim_by_townshaip_df
        if len(slim_by_townshaip_df['district'].value_counts()) > 1:
            slim_by_district_df = pd.DataFrame(columns=address_list.columns)
            for token in tokens:
                if len(token) > 1 and token in list(slim_by_townshaip_df['district']):
                    slim_by_district_df = pd.concat(
                        [slim_by_district_df, self.slim_by_domain(slim_by_townshaip_df, 'district', token)], axis=0)

        # 根据street + city
        slim_by_city_df = slim_by_district_df
        print(slim_by_district_df)
        if len(slim_by_district_df['city'].value_counts()) > 1:
            slim_by_city_df = pd.DataFrame(columns=address_list.columns)
            for token in tokens:
                if len(token) > 1 and token in list(slim_by_district_df['city']):
                    slim_by_city_df = pd.concat(
                        [slim_by_city_df, self.slim_by_domain(slim_by_district_df, 'city', '广州')], axis=0)

        # 根据street + province
        slim_by_province_df = slim_by_city_df
        if len(slim_by_townshaip_df['province'].value_counts()) > 1:
            slim_by_province_df = pd.DataFrame(columns=address_list.columns)
            for token in tokens:
                if len(token) > 1 and token in list(slim_by_city_df['province']):
                    slim_by_province_df = pd.concat(
                        [slim_by_province_df, self.slim_by_domain(slim_by_city_df, 'province', token)], axis=0)

        # 判断数据空列
        if len(slim_by_province_df['street'].value_counts()) > 1:
            slim_by_province_df = slim_by_province_df[
                (slim_by_province_df['street'] != slim_by_province_df['district'])]

        if len(slim_by_province_df['street'].value_counts()) > 1:
            slim_by_province_df = slim_by_province_df[
                (slim_by_province_df['street'] != slim_by_province_df['township'])]

        slim_by_province_df.drop_duplicates(keep='first', inplace=True)

        if slim_by_province_df.shape[0] == 0:
            slim_by_province_df = slim_by_street_df

        # print(slim_by_province_df)
        return slim_by_province_df

    def judge_from_street_and_streetnum(self, dataframe, sentence_sample):
        sentences = []

        # 反向匹配
        max_lens = 0
        for index, street, streetnum in zip(dataframe.index, list(dataframe['street']), list(dataframe['street_num'])):
            target = str(street) + '' + str(streetnum)
            if sentence_sample.__contains__(target) and len(target) > max_lens:
                max_lens = len(target)

                if len(sentences) == 0:
                    pass
                else:
                    sentences.pop()
                sentences.append(dataframe.loc[index])

        # 四川省成都市青白江区
        # 四川省成都市青白江区 77号
        if len(sentences) > 0:
            return sentences.pop()
        else:
            return []

    def judge_address(self, address_list, tokens, sentence):
        # 根据street, township, district三个关键字缩小数据的查询范围
        dataframe = self.slim_data(address_list, tokens)
        dataframe.drop_duplicates(keep='first', inplace=True)
        result = self.judge_from_street_and_streetnum(dataframe, sentence)

        if len(pd.DataFrame(result).columns.values) > 0:
            index = pd.DataFrame(result).columns.values[0]
            formal_result = self.origin_address_list.iloc[index]
        else:
            formal_result = result

        return formal_result


def get_tokens_and_sents(input_file):
    tokens = []
    sents = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            lines = line.split('$')
            tokens.append(lines[0].strip())
            sents.append(lines[1].strip())

    return tokens, sents


def main():
    testset = AddressDict('data/Standara_Address_Data_Of_A.csv')
    testset.address_list = testset.formal_missing_token(testset.address_list)
    address_list = testset.address_list
    jieba.load_userdict('data/address_dict.txt')

    results = []
    tokens, sentences = get_tokens_and_sents('data/all_txt.txt')

    # get results
    for i, token, sentence in zip(range(1, 501), tokens, sentences):
        print("process " + str(i) + ".html")
        token_jieba = list(jieba.cut(token))
        result = testset.judge_address(address_list, token_jieba, sentence)

        results.append(list(result))

    # output results
    with open('data/results_all_4.csv', 'w', encoding='utf-8') as f_write:
        for i, lines in zip(range(1, 501), results):
            if len(lines) > 5:
                output_line = str(i) + '.html,' + lines[0] + '$' + lines[1] + '$' + lines[2] + '$' + lines[3] + '$' + str(lines[4]) + '$' + str(
                lines[5]) + '$' + str(lines[6]) + '$' + str(lines[7])
            else:
                output_line = str(i) + '.html,'
            f_write.write(output_line + '\n')

        print("Done")


def debug():
    # 输入单个地址检查是否识别正确
    # tokens代表该html中所有与地名相关的token
    # sentences代表该html中，street出现的那句话
    testset = AddressDict('data/Standara_Address_Data_Of_A.csv')
    testset.address_list = testset.formal_missing_token(testset.address_list)
    address_list = testset.address_list
    jieba.load_userdict('data/address_dict.txt')
    tokens = list(jieba.cut('张三生活2220大安路文化广州'))
    sentences = '现居广州大安路3号这20年来'

    results = testset.judge_address(address_list, tokens, sentences)
    lines = list(results)
    # for token in tokens:
    #     print(token)
    if len(lines) == 0:
        pass
    else:
        print(lines[0] + '$' + lines[1] + '$' + lines[2] + '$' + lines[3] + '$' + str(lines[4]) + '$' + str(
            lines[5]) + '$' + str(lines[6]) + '$' + str(lines[7]))


if __name__ == '__main__':
    # main()
    debug()

