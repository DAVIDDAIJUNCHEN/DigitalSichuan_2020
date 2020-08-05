
import re
from operator import itemgetter, attrgetter

def emb_numbers(s):
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(s)
    pieces[1::2] = map(int, pieces[1::2])
    pieces.extend([-1, -1, -1])
    pieces[2:3] = pieces[3:2]
    pieces[3:4] = pieces[4:3]

    return pieces


def sort_strings_with_emb_numbers(alist):
    aux = [(emb_numbers(s), s) for s in alist]
    aux.sort()
    return [s for __,s in aux]


def sort_strings_with_emb_numbers2(alist):
    return sorted(alist, key=emb_numbers)


def zhaobutong():
    dicts_1 = {}
    dicts_2 = {}
    with open('results/e_sol.csv', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('\n', '')
            tokens = line.split(',')
            if len(tokens) >= 3:
                dicts_1[tokens[1]] = tokens[2]

    with open('results/0804-1_results.csv', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('\n', '')
            tokens = line.split(',')
            if len(tokens) >= 2:
                if len(tokens[1]) > 5:
                    dicts_2[tokens[0]] = tokens[1]

    for key in dicts_1.keys():
        if key in dicts_2.keys():
            continue
        else:
            print(key)


if __name__ == '__main__':
    # 790
    # 王圣堂莲塘街 越秀区 常德市 矿泉街道 澧县$现居王圣堂莲塘街1号档
    s = ['31号', '33-25号', '33-之23号', '34号', '30号']
    s = sort_strings_with_emb_numbers2(s)

    print(s)
