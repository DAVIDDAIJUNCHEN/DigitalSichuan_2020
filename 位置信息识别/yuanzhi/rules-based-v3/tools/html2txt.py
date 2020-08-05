import re
from html import unescape
import os


def html_to_plain_text(html):
    text = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
    text = re.sub('<a\s.*?>', ' HYPERLINK ', text, flags=re.M | re.S | re.I)
    text = re.sub('<.*?>', '', text, flags=re.M | re.S)
    text = re.sub(r'(\s*\n)+', '\n', text, flags=re.M | re.S)
    return unescape(text)


def html2txt(dirs_inputs, dirs_output):
    lists = os.listdir(dirs_inputs)
    for i in range(0, len(lists)):
        print("processing {}.html".format(i))

        path_input = os.path.join(dirs_inputs, lists[i])
        with open(path_input, 'r', encoding='utf-8') as f:
            text = html_to_plain_text(f.read())
            path_output = dirs_output + lists[i].replace('html', 'txt')

            with open(path_output, 'w', encoding='utf-8') as f_write:
                texts = text.split()
                for text_txt in texts:
                    f_write.write(text_txt)
                    f_write.write('\n')


if __name__ == '__main__':
    dirs_inputs = "../data/html"
    dirs_output = "../data/txt"

    html2txt(dirs_inputs, dirs_output)

    print("Write Done")
