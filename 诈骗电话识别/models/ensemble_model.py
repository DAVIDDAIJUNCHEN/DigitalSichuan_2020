#/usr/bin/env python3

# import modules
import pandas as pd

def ensemble(dict_model_acc, test_design, method='vote'):
    """ensemble models according to accuracies
    :param dict_model_acc: {'model_name': (model, acc)}
    :param test_design:  X = [[x11, x12, ..., x1p], ..., [xn1, xn2, ..., xnp]]
    :param method: vote | avg_unif | avg_softmax | grid_search
    """
    pred_models_dict = {}
    pred_models_lst = []

    for name_model, (model, acc) in dict_model_acc.items():
        pred_model = model.predict(test_design).tolist()
        pred_models_dict[name_model] = pred_model
        pred_models_lst.append(pred_model)

    pred_model_df = pd.DataFrame(pred_models_lst)

    if method == 'vote':
        pred_vote_df = pred_model_df.mode()
        pred_vote_lst = list(pred_vote_df.loc[0, :])

        return pred_vote_lst
#    elif method == 'avg_unif':





# debug part
#dict_model_acc = {'logit_1': ('logit', 1), 'logit_2':('logit2', 2)}
#ensemble(dict_model_acc, 'a')