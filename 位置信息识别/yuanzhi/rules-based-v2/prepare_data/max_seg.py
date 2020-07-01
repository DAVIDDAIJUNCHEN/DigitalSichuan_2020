# coding:utf-8
import pandas as pd
import nltk
import time

class PsegMax:
    def __init__(self, dict_path):
        self.entity_dict, self.max_len = self.load_entity(dict_path)

    def load_entity(self, dict_path):
        """
        加载实体词典
        """

        entity_list = []
        max_len = 0

        """ 实体词典: {'肾抗针': 'DRU', '肾囊肿': 'DIS', '肾区': 'REG', '肾上腺皮质功能减退症': 'DIS', ...} """
        df = pd.read_csv(dict_path, sep='\t', header=None, names=["entity", "tag"], dtype={'entity': str, 'tag': str})
        df.apply(lambda x: str(x))
        entity_dict = {str(entity).strip(): str(tag).strip() for entity, tag in df.values.tolist()}

        """ 计算词典中实体的最大长度 """
        df["len"] = df["entity"].apply(lambda x: len(x))
        max_len = max(df["len"])

        return entity_dict, max_len

    def max_forward_seg(self, sent):
        """
        前向最大匹配实体标注
        """
        words_pos_seg = []
        sent_len = len(sent)

        while sent_len > 0:

            """ 如果句子长度小于实体最大长度，则切分的最大长度为句子长度 """
            max_len = min(sent_len, self.max_len)

            """ 从左向右截取max_len个字符，去词典中匹配 """
            sub_sent = sent[:max_len]

            while max_len > 0:

                """ 如果切分的词在实体词典中，那就是切出来的实体 """
                if sub_sent in self.entity_dict:
                    tag = self.entity_dict[sub_sent]
                    words_pos_seg.append((sub_sent, tag))
                    break

                elif max_len == 1:

                    """ 如果没有匹配上，那就把单个字切出来，标签为O """
                    tag = "O"
                    words_pos_seg.append((sub_sent, tag))
                    break

                else:

                    """ 如果没有匹配上，又还没剩最后一个字，就去掉右边的字,继续循环 """
                    max_len -= 1
                    sub_sent = sub_sent[:max_len]

            """ 把分出来的词（实体或单个字）去掉，继续切分剩下的句子 """
            sent = sent[max_len:]
            sent_len -= max_len

        return words_pos_seg

    def max_backward_seg(self, sent):
        """
        后向最大匹配实体标注
        """

        words_pos_seg = []
        sent_len = len(sent)

        while sent_len > 0:

            """ 如果句子长度小于实体最大长度，则切分的最大长度为句子长度 """
            max_len = min(sent_len, self.max_len)

            """ 从右向左截取max_len个字符，去词典中匹配 """
            sub_sent = sent[-max_len:]

            while max_len > 0:

                """ 如果切分的词在实体词典中，那就是切出来的实体 """
                if sub_sent in self.entity_dict:
                    tag = self.entity_dict[sub_sent]
                    words_pos_seg.append((sub_sent, tag))
                    break

                elif max_len == 1:

                    """ 如果没有匹配上，那就把单个字切出来，标签为O """
                    tag = "O"
                    words_pos_seg.append((sub_sent, tag))
                    break

                else:

                    """ 如果没有匹配上，又还没剩最后一个字，就去掉右边的字,继续循环 """
                    max_len -= 1
                    sub_sent = sub_sent[-max_len:]

            """ 把分出来的词（实体或单个字）去掉，继续切分剩下的句子 """
            sent = sent[:-max_len]
            sent_len -= max_len

        """ 把切分的结果反转 """
        return words_pos_seg[::-1]

    def max_biward_seg(self, sent):
        """
        双向最大匹配实体标注
        """

        """ 1: 前向和后向的切分结果 """
        words_psg_fw = self.max_forward_seg(sent)
        words_psg_bw = self.max_backward_seg(sent)

        """ 2: 前向和后向的词数 """
        words_fw_size = len(words_psg_fw)
        words_bw_size = len(words_psg_bw)

        """ 3: 前向和后向的词数，则取词数较少的那个 """
        if words_fw_size < words_bw_size: return words_psg_fw

        if words_fw_size > words_bw_size: return words_psg_bw

        """ 4: 结果相同，可返回任意一个 """
        if words_psg_fw == words_psg_bw: return words_psg_fw

        """ 5: 结果不同，返回单字较少的那个 """
        fw_single = sum([1 for i in range(words_fw_size) if len(words_psg_fw[i][0]) == 1])
        bw_single = sum([1 for i in range(words_fw_size) if len(words_psg_bw[i][0]) == 1])

        if fw_single < bw_single:
            return words_psg_fw
        else:
            return words_psg_bw


if __name__ == "__main__":


    dict_path = "address_dicts_data/all_address_dict.csv"
    text1 = ""
    for i in range(1):
        text = "黄种人的命也是命！韩国广州模特拒绝声援黑人来，美经在世界范围内引起了轰动，许多公众人物公开为黑人发声，希望为死去的弗洛伊德讨回公道。同时，也想通过这一悲剧来给警醒世界各国，“种族主义”不应该被提倡，有色人种也不该被区别对待，每个人都应该得到平等的待遇，肤色或国籍不应该成为他们被歧视的理由！大部分人都为黑人的死发出了抗议的声音，但是其中韩国的一位模特却发出了不同的声音，该模特拒绝为黑人的遭遇发声，理由是，作为黄种人的自己也同样被区别对待着！据了解，该模特名叫妮基，是一名在美国的韩裔模特，要知道，目前美国的需多公共人物都公开表示了对黑人的支持，有的甚至还捐赠了大笔资金用来支持黑人。那么妮基为什么要与他人背道而驰呢？其实妮基也认同“生而平等”的观念，但是从他自己的亲身经历来讲，妮基认为黑人对黄种人的态度也是非常恶劣的，所以妮基拒绝支持黑人，因为他认为黄种人也应该享受平等的待遇！“人人生而平等”的观点早在十八世纪就被提出来了，但是直到目前，“种族歧视”仍然刻在某些白种人的骨子里。真希望有一天，肤色不再是人与人之间的隔阂，不仅是黑人，黄种人也能收到公平的待遇，虽然目前的黑人事件仍在不断发酵，但是希望对于黄种人的遭遇也能早点被世界看见！对于“种族歧视”，大家有什么想说的呢？欢迎大家留言参与讨论！"
        text1 = text1 + text

    print(len(text1))
    t0 = time.time()
    psg = PsegMax(dict_path)
    words_psg = psg.max_biward_seg(text1)

    print(words_psg)
    print(time.time()-t0)