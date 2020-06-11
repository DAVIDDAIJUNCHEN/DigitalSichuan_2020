import jieba
import re
from lxml import etree
from html import unescape
import os


def get_dict():
    all_poi_tokens = []
    street_tokens = []
    with open('data/address_dict.txt', 'r', encoding='utf-8') as f:
        for poi in f.readlines():
            all_poi_tokens.append(poi.strip())

    with open('data/street_tokens.txt', 'r', encoding='utf-8') as f:
        for street in f.readlines():
            street_tokens.append(street.strip())

    return all_poi_tokens, street_tokens

def clean_single_txt(input_file):
    # input_file = 'data/txt/175.txt'
    jieba.load_userdict('data/address_dict.txt')
    sentences = []
    all_tokens = set()
    all_poi_dict, street_dict = get_dict()
    target_sentence = []

    # 去除文本的标点符号，将其转换为单句
    # pattern = r',|\.|/|;|\?|:|!|，|。|、|；|‘|’|【|】|·|！|…|'
    pattern = r',|\.|/|;|\?|:|!|，|。|；|‘|’|【|】|·|！|…'
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            sentences.extend(re.split(pattern, line))

    for line in sentences:
        tokens = jieba.cut(line)
        flag = 0
        for token in tokens:
            # print(token)
            if len(token) > 1:
                for poi in all_poi_dict:
                    if poi.__contains__(token):
                        # print(token)
                        all_tokens.add(token)

                for street in street_dict:
                    if street == token:
                        target_sentence.append(''.join(line))

    return all_tokens, target_sentence


def clean_all():
    rootdir = r"C:\YuanZhi\PycharmProjects\poi-distinguish\data\txt"
    clean_root_dir = r"/poi-distinguish/data/txt_clean"
    list = os.listdir(rootdir)

    for file in list:
        path = os.path.join(rootdir, file)
        tokens, sentences = clean_single_txt(path)
        print(file)

        output_path = os.path.join(clean_root_dir, file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(''.join(tokens))
            f.write('\n')
            for sens in sentences:
                f.write(sens)
                f.write('\n')

    print("Write Done")


def html_to_plain_text(html):
    text = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
    text = re.sub('<a\s.*?>', ' HYPERLINK ', text, flags=re.M | re.S | re.I)
    text = re.sub('<.*?>', '', text, flags=re.M | re.S)
    text = re.sub(r'(\s*\n)+', '\n', text, flags=re.M | re.S)
    return unescape(text)


def html2txt():

    rootdir = r"C:\YuanZhi\PycharmProjects\poi-distinguish\data\html"
    list = os.listdir(r"/poi-distinguish/data/html")
    for i in range(0, len(list)):
        file_path = os.path.join(rootdir, list[i])
        with open(file_path, 'r', encoding='utf-8') as f:
            text = html_to_plain_text(f.read())
            output = 'data/txt/'+list[i].replace('html', 'txt')
            with open(output, 'w', encoding='utf-8') as f_write:
                texts = text.split()
                for text_txt in texts:
                    f_write.write(text_txt)
                    f_write.write('\n')

    print("Write Done")


def convert_all_txt():
    contents = []
    for i in range(1, 501):
        input = 'data/txt_clean/' + str(i) + '.txt'
        content = ""
        with open(input, 'r', encoding='utf-8') as f:
            for j, line in zip(range(4), f):
                if j == 0:
                    content += line.replace('\n', '')
                elif len(line) == 0:
                    pass
                else:
                    content = content + '$' + line.replace('\n', '')
                    break

        contents.append(content)

    with open('data/all_txt.txt', 'w', encoding='utf-8') as f_write:
        for line in contents:
            f_write.write(line)
            f_write.write('\n')

    print("write Done")


def get_tokens_and_sents(input_file):
    tokens = []
    sents = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            lines = line.split('$')
            tokens.append(lines[1].strip())
            sents.append(lines[1].strip())

    return tokens, sents

def main():
    # html2txt()
    # clean_all()
    convert_all_txt()


if __name__ == '__main__':
    main()
