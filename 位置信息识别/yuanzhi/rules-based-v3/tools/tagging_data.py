from tools.tokenizer import PsegMax
import os


class TaggingData(object):
    def __init__(self, dicts_path):
        self.street = dicts_path
        self.psg = PsegMax(dicts_path)

    def _read_file(self, file):
        res = []
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.read():
                res.append(line)

        return res

    def _write_to_files(self, files, tokens):
        with open(files, 'a+', encoding='utf-8') as f_write:
            for tuples in tokens:
                if tuples[0].strip() == "":
                    continue

                if tuples[1] == 'O':
                    f_write.write(tuples[0] + " " + tuples[1] + "\n")
                else:
                    f_write.write(str(list(tuples[0])[0]) + " B-" + tuples[1] + "\n")
                    for word in list(tuples[0])[1:]:
                        f_write.write(str(word) + " I-" + tuples[1] + "\n")

            f_write.write("\n")

    def tagging_data(self, dirs, target_files):
        files = os.listdir(dirs)
        for file in files:
            res = self._read_file(os.path.join(dirs, file))
            for line in res[1:]:
                line = line.replace('\n', '')
                lines = line.split('，')
                for line_1 in lines:
                    msg_tokens = self.psg.max_biward_seg(line_1)
                    self._write_to_files(target_files, msg_tokens)


if __name__ == '__main__':
    dict_path = "../dicts/ALL.dict"
    msg = PsegMax(dict_path)
    tag_data = TaggingData(dict_path)

    dirs = "../data/tag/test"
    target_files = "../data/tag/example.test"
    tag_data.tagging_data(dirs, target_files)

