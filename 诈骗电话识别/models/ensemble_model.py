#/usr/bin/env python3

# import modules
import pandas as pd
import numpy as np

def ensemble(dict_model_acc, test_design, method='vote'):
    """ensemble models according to accuracies
    :param dict_model_acc: {'model_name': (model, acc)}
    :param test_design:  X = [[x11, x12, ..., x1p], ..., [xn1, xn2, ..., xnp]]
    :param method: vote | avg_unif | avg_softmax | grid_search
    """
    pred_models_dict = {}
    pred_models_lst = []
    prob_models_dict = {}
    prob_models_lst = []
    prob1_models_lst = []
    acc_lst = []
    test_design = np.array(test_design)

    for name_model, (model, acc) in dict_model_acc.items():
        pred_model = model.predict(test_design).tolist()
        pred_models_dict[name_model] = pred_model
        pred_models_lst.append(pred_model)

        acc_lst.append(acc)

    pred_models_df = pd.DataFrame(pred_models_lst)

    if method == 'vote':
        pred_vote_df = pred_models_df.mode()
        pred_vote_lst = list(pred_vote_df.loc[0, :])

        return pred_vote_lst

    prob_models_dict = {}
    prob_models_lst = []
    prob1_models_lst = []
    acc_lst = []

    for name_model, (model, acc) in dict_model_acc.items():
        prob_model = model.predict_proba(test_design)
        prob1_model = np.array(prob_model)[:, 1].tolist()
        prob_models_dict[name_model] = prob_model
        prob1_models_lst.append(prob1_model)
        prob_models_lst.append(prob_model)

        acc_lst.append(acc)

    prob1_models_df = pd.DataFrame(prob1_models_lst)

    if method == 'avg_unif':
        prob1_avgunif_lst = list(prob1_models_df.mean())
        pred_avgunif_lst = [int(score > 0.5) for score in prob1_avgunif_lst]

        return pred_avgunif_lst, prob1_avgunif_lst
    elif method == 'avg_softmax':
        sum_exp_acc = sum(np.exp(acc_lst))
        acc_softmax = [np.exp(item) / sum_exp_acc for item in acc_lst]
        prob1_weighted_df = prob1_models_df.multiply(acc_softmax, axis='rows')
        prob1_softmax_lst = list(prob1_weighted_df.sum())
        pred_softmax_lst = [int(score > 0.5) for score in prob1_softmax_lst]

        return pred_softmax_lst, prob1_softmax_lst

    #elif method == 'grid_search':