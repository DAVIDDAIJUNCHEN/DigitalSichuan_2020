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
            1: street+street_num+locationx+locationy 可以合并在一起
            2:
        """
        self.input_file = input_file
        self.address_list = pd.read_csv(input_file, sep='\t', dtype={'locationx': str, 'locationy': str})
        self.origin_address_list = self.address_list.copy().fillna('')
        self.province = self.address_list['province']
        self.city = self.address_list['city']
        self.district = self.address_list['district']
        self.township = self.address_list['township']
        self.street = self.address_list['street']
        self.street_num = self.address_list['street_num']
        self.locationx = self.address_list['locationx']
        self.locationy = self.address_list['locationy']

    def formal_missing_token(self, dataframe):
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

        # print(dataframe[dataframe['street_num'].isnull() == True])
        # print(dataframe[dataframe['street'].isnull() == True])
        # print(dataframe[dataframe['district'].isnull() == True])
        # print(dataframe[dataframe['township'].isnull() == True])
        # print(dataframe[dataframe['locationx'].isnull() == True])
        # print(dataframe[dataframe['locationy'].isnull() == True])

        return dataframe

    def slim_by_domain(self, dataframe, domain, token):
        if domain not in dataframe.columns:
            assert "Not Found columns: {}".format(domain)
            return dataframe
        if domain == 'district':
            return dataframe[dataframe[domain].str.contains(token)]
        else:
            return dataframe[dataframe[domain] == token]

    def slim_data(self, tokens):
        # 根据street筛选数据
        slim_by_street_df = self.address_list
        for token in tokens:
            if token in list(self.address_list['street']):
                slim_by_street_df = self.slim_by_domain(self.address_list, 'street', token)

        # 如果上面得出的数据里，township列不唯一，则继续根据street+township 筛选数据
        slim_by_townshaip_df = slim_by_street_df
        if len(slim_by_street_df['township'].value_counts()) > 1:
            for token in tokens:
                if token in list(slim_by_street_df['township']):
                    slim_by_townshaip_df = self.slim_by_domain(slim_by_street_df, 'township', token)

        slim_by_district_df = slim_by_townshaip_df
        if len(slim_by_townshaip_df['district'].value_counts()) > 1:
            for token in tokens:
                if len(token) > 1 and token in list(slim_by_district_df['district']):
                    slim_by_district_df = self.slim_by_domain(slim_by_townshaip_df, 'district', token)

        return slim_by_district_df

    def judge_from_street_and_streetnum(self, dataframe, sentence):
        sentences = []

        for index, street, streetnum in zip(dataframe.index, list(dataframe['street']), list(dataframe['street_num'])):
            target = str(street) + '' + str(streetnum)
            if sentence.__contains__(target):
                sentences.append(dataframe.loc[index])

        # 四川省成都市青白江区
        # 四川省成都市青白江区 77号
        if len(sentences) > 1:
            sentence = sentences.pop()
            if sentence['street_num'] == '':
                pass
            else:
                return sentence
        if len(sentences) > 0:
            return sentences.pop()
        else:
            return []

    def judge_address(self, tokens, sentences):
        # 根据street, township, district三个关键字缩小数据的查询范围
        dataframe = self.slim_data(tokens)
        results = []
        for sentence in sentences:
            results.append(self.judge_from_street_and_streetnum(dataframe, sentence))

        for result in results:
            if len(result) == 0:
                pass
            else:
                result = self.origin_address_list.iloc[pd.DataFrame(result).columns.values[0]]
                return result
        return []


def main():
    # 都和某某号来做对比
    testset = AddressDict('data/Standara_Address_Data_Of_A.csv')
    testset.address_list = testset.formal_missing_token(testset.address_list)
    jieba.load_userdict('data/address_dict.txt')

    sentences = []
    results = []
    for i in range(101, 501):
        print("process "+str(i)+'html')
        with open('data/txt_clean/' + str(i) + '.txt', 'r', encoding='utf-8') as f:
            for j, line in zip(range(4), f):
                if j == 0:
                    tokens = list(jieba.cut(line))
                elif j > 0 and len(line) > 0:
                    sentences.append(line)
            results.append(testset.judge_address(tokens, sentences))

    with open('data/results_all_1.txt', 'w', encoding='utf-8') as f_write:
        for i, result in zip(range(101, 501), results):
            if len(result) == 0:
                line = str(i) + '.html, '
            else:
                lines = list(result)
                line = str(i) + '.html,' + lines[0] + '$' + lines[1] + '$' + lines[2] + '$' + lines[3] + '$' + str(lines[4]) + '$' + str(lines[5]) + '$' + str(lines[6]) + '$' + str(lines[7])
                print(line)
            f_write.write(line)
            f_write.write('\n')
    # tokens = list(jieba.cut("10街道天桥湖里区张三政府市民金湖路厦门禾山街道繁荣美食"))
    # sentences = ["”地处湖里区禾山街道金湖路397号夫妻肺片总店负责人王钦锐告诉记者"]


if __name__ == '__main__':
    # main()


    testset = AddressDict('data/Standara_Address_Data_Of_A.csv')
    testset.address_list = testset.formal_missing_token(testset.address_list)
    jieba.load_userdict('data/address_dict.txt')
    tokens = jieba.cut('福州30吴航街道西关街长乐区')
    sentences = ['”福州长乐区吴航街道西关街156号']

    results = testset.judge_address(tokens, sentences)
    lines = list(results)
    print(lines[0] + '$' + lines[1] + '$' + lines[2] + '$' + lines[3] + '$' + str(lines[4]) + '$' + str(lines[5]) + '$' + str(lines[6]) + '$' + str(lines[7]))

