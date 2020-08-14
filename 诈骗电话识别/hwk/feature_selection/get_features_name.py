import yaml
def get_features_name_from_config(config_yml):
    feature_names = []
    with open(config_yml) as file:
        def_para = yaml.load(file)
        def_para_columns = {}
        def_para_features = {}

        def_para_name = def_para['name']
        def_para_columns = def_para['columns'][0]
        for item in def_para['features']:
            for t in item:
                feature_names.append(item[t][0]['name'])
    print(999)
    return feature_names



if __name__=="__main__":
    train_config_yml = '../configs/distinguished_config_train.yml'
    feature_names=get_features_name_from_config(train_config_yml)

    print(8)