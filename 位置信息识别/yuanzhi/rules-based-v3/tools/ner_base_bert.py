import kashgari
import re


class BertNerBilstmCrf(object):
    def __init__(self, config):
        self.model = kashgari.utils.load_model(config)

    def cut_text(self, text, lenth):
        textArr = re.findall('.{' + str(lenth) + '}', text)
        textArr.append(text[(len(textArr) * lenth):])
        return textArr

    def extract_labels(self, text, ners):
        ner_reg_list = []
        if ners:
            new_ners = []
            for ner in ners:
                new_ners += ner;
            for word, tag in zip([char for char in text], new_ners):
                if tag != 'O':
                    ner_reg_list.append((word, tag))

        # 输出模型的NER识别结果
        labels = {}
        if ner_reg_list:
            for i, item in enumerate(ner_reg_list):
                if item[1].startswith('B'):
                    label = ""
                    end = i + 1
                    while end <= len(ner_reg_list) - 1 and ner_reg_list[end][1].startswith('I'):
                        end += 1

                    ner_type = item[1].split('-')[1]

                    if ner_type not in labels.keys():
                        labels[ner_type] = []

                    label += ''.join([item[0] for item in ner_reg_list[i:end]])
                    labels[ner_type].append(label)

        return labels


if __name__ == '__main__':
    model = BertNerBilstmCrf("../data/ner/BERT-NER-CRF.h5")

    while True:
        text_input = input('sentence: ')
        texts = model.cut_text(text_input, 100)
        ners = model.model.predict([[char for char in text] for text in texts])
        print(ners)
        labels = model.extract_labels(text_input, ners)
        print(labels)
