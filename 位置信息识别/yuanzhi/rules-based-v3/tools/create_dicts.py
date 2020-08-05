import pandas as pd

if __name__ == '__main__':
    # 根据标准地址数据库构建词典
    # 省、市、区、街道、路
    input_file = r'C:\WorkFile\NLPCompetition\poiDistinguish\secondRoundData\address_normal_data.csv'
    address_dict = {}
    address_data = pd.read_csv(input_file, sep='\t')

    # 'province', 'city', 'district', 'township', 'street'
    tokens = ['district']

    for token in tokens:
        for line in address_data[token]:
            address_dict[str(line)] = 1

    with open('../dicts/DIS.dict', 'w', encoding='utf-8') as f:
        for key in address_dict.keys():
            f.write(str(key) + "\t" +"DIS" + '\n')

    print("Write Done")