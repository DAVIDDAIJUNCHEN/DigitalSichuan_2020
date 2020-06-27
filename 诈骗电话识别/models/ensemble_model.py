#/usr/bin/env python3

def ensemble(dict_model_acc, test_design, method='vote'):
    """ensemble models according to accuracies
    :param dict_model_acc: {'model_name': (model, acc)}
    :param test_design:  X = [[x11, x12, ..., x1p], ..., [xn1, xn2, ..., xnp]]
    :param method: vote | avg_unif | avg_softmax | grid_search
    """
    pred_models = {}
    for name_model, (model, acc) in dict_model_acc.items():
         pred_models[name_model] = model.predict(test_design).tolist()

    if method == 'vote':





# debug part
dict_model_acc = {'logit_1': ('logit', 1), 'logit_2':('logit2', 2)}
ensemble(dict_model_acc, 'a')