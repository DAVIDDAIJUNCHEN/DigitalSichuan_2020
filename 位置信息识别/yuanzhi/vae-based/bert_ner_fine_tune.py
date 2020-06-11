import kashgari
from kashgari.corpus import ChineseDailyNerCorpus
from kashgari.tasks.labeling import BiLSTM_Model
from kashgari.embeddings import BERTEmbedding

train_x, train_y = ChineseDailyNerCorpus.load_data('train')
valid_x, valid_y = ChineseDailyNerCorpus.load_data('validate')
test_x, test_y  = ChineseDailyNerCorpus.load_data('test')

bert_embed = BERTEmbedding('data/chinese_wwm_ext_L-12_H-768_A-12',
                           task=kashgari.LABELING,
                           sequence_length=100)

model = BiLSTM_Model(bert_embed)
model.fit(train_x, train_y, valid_x, valid_y, epochs=2, batch_size=512)
model.save('BERT-NER.h5')