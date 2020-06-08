#!/usr/bin/env python3

# import modules
from sklearn.metrics import f1_score

def evaluate(golden_truth, pred, model=None):
    """wrap up evaluation methods and print information"""
    f1 = f1_score(golden_truth, pred, average='micro')
    if model == None:
        print('F1 score is {}'.format(f1))
    else:
        assert type(model) == str
        print(model + ': F1 score is {}'.format(f1))

#def plot_acc()