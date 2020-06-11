import pandas as pd
from address_dict import AddressDict

if __name__ == '__main__':
    input_file = 'data/Standara_Address_Data_Of_A.csv'
    address_dict = {}
    address_data = pd.read_csv(input_file, sep='\t')
    obj = AddressDict(input_file)
    address_data = obj.formal_missing_token(address_data)

    # 'province', 'city', 'district', 'township'
    tokens = ['street']

    for token in tokens:
        for line in address_data[token]:
            address_dict[line] = 1

    with open('data/street_tokens.txt', 'w', encoding='utf-8') as f:
        for key in address_dict.keys():
            f.write(str(key))
            f.write("\n")

    print("Write Done")