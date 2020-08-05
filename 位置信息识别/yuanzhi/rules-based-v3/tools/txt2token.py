import os
import re
from tools.tokenizer import PsegMax


def get_dict():
    all_poi_tokens = []
    street_tokens = []
    with open('../dicts/ALL.dict', 'r', encoding='utf-8') as f:
        for poi in f.readlines():
            all_poi_tokens.append(poi.split()[0])

    with open('../dicts/STR.dict', 'r', encoding='utf-8') as f:
        for street in f.readlines():
            street_tokens.append(street.split()[0])

    return all_poi_tokens, street_tokens


def remove_dup(sentences, tokens=set(), method='sentence'):
    pattern = '\d*[号栋幢巷弄座]'
    if method == 'sentence':
        for line in sentences:
            if len(re.findall(pattern, line)) == 0:
                sentences.remove(line)

        return sentences

    elif method == 'token':
        if len(sentences) == 0:
            assert "sentences is 0 numbers"

        re_strs = re.findall(pattern, sentences[0])
        if len(re_strs) == 0:
            return tokens

        min_dis = 100
        tmp_token = ""
        for token in tokens:
            distance = sentences[0].find(re_strs[0]) - sentences[0].find(token)
            if 0 < distance < min_dis:
                min_dis = distance
                tmp_token = token

        return [tmp_token]


def clean_single_txt(input_file, token_tools):
    psg = token_tools
    all_tokens = set()
    str_tokens = set()
    str_sentence = []
    tow_sentence = []

    target_sentence = ""
    target_token = []

    # 去除文本的标点符号，将其转换为单句
    sentences = []
    pattern = r',|\.|/|;|\?|:|!|，|。|；|·|！|…'
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            sentences.extend(re.split(pattern, line))

    # 对上面得到对句子进行分词，得到地址名词和包含道路名（如道路名为空则包含街道名）的句子
    for line in sentences:
        tokens = psg.max_biward_seg(line)
        for token, tag in tokens:
            if tag != 'O':
                if tag == 'STR':
                    str_tokens.add(token)
                    str_sentence.append(line)
                elif tag == 'TOW':
                    target_token.append(token)
                    tow_sentence.append(line)
                else:
                    target_token.append(token)
                    all_tokens.add(token)

    # 得到的句子和道路名可能有多条，对他们分别只保留一条
    # 逻辑：只用判断str和tow两个token所在的句子
    # 句子的取法： 如果该句子包含号、栋这些信息，则取出来
    # 道路名的取法：判断谁离路号近，就取谁
    if len(str_sentence) > 1:
        str_sentence = remove_dup(str_sentence)
        target_sentence = str_sentence[0]
    elif len(str_sentence) == 0:
        if len(tow_sentence) > 1:
            tow_sentence = remove_dup(tow_sentence)
            target_sentence = tow_sentence[0]
    else:
        target_sentence = str_sentence[0]

    if len(str_sentence) >= 1:
        if len(str_tokens) > 1:
            str_tokens = remove_dup(str_sentence, str_tokens, method='token')
    elif len(str_sentence) == 0:
        str_tokens = remove_dup(tow_sentence, str_tokens, method='token')

    target_token.extend(list(all_tokens))
    target_token.extend(list(str_tokens))

    return " ".join(set(target_token)), target_sentence


def clean_all_txt(input_dirs, output_files, tools):
    contents = []

    for i in range(1, 10001):
        print("Process {}.txt".format(i))
        tokens, sentence = clean_single_txt(os.path.join(input_dirs, str(i)+'.txt'), token_tools=tools)
        content = tokens+"$"+sentence
        contents.append(str(i)+".html: "+content)

        if i % 1000 == 0:
            with open(output_files, 'a+', encoding='utf-8') as f_write:
                for line in contents:
                    f_write.write(line.replace('\n', ''))
                    f_write.write('\n')
            contents = []

    print("write Done")


def debug():
    tools = PsegMax("../dicts/ALL.dict")
    tokens, sentences = clean_single_txt("../data/txt/487.txt", token_tools=tools)
    print("tokens: {}".format(tokens))
    print("sentences: {}".format(sentences))


def main():
    tools = PsegMax("../dicts/ALL.dict")
    output_files = "../data/tokens_and_sentences/4tokens_and_sentences.txt"
    input_dirs = "../data/txt"

    clean_all_txt(input_dirs, output_files, tools)


if __name__ == '__main__':
    # debug()
    main()
