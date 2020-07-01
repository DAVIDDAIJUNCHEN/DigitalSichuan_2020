import pandas as pd

if __name__ == '__main__':
    input_file = 'address_dicts_data/Standara_Address_Data_Of_A.csv'
    address_dict = {}
    address_data = pd.read_csv(input_file, sep='\t')
    labels = {'province': 'PROV', 'city': 'CIT', 'district': 'DIS', 'township': 'TOW', 'street': 'STR', 'street_num': 'STRN'}

    # 'province', 'city', 'district', 'township'
    # tokens = ['province', 'city', 'district', 'township', 'street', 'street_num']
    tokens = ['township']

    for token in tokens:
        address_dict = {}
        for line in address_data[token]:
            address_dict[line] = 1
            if str(line).endswith('镇') or str(line).endswith('乡'):
                address_dict["".join(list(line)[:-1])] = 1

        with open('address_dicts_data/' + str(token) + '_dict.csv', 'w', encoding='utf-8') as f:
            for key in address_dict.keys():
                f.write(str(key) + '\t' + labels[str(token)])
                f.write("\n")

    print("Write Done")