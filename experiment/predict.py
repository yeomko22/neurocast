import numpy as np
from util import util
from model.als import ALS
import os
from util import dataload

def binarize(predict_result):
    predict_binary = np.copy(predict_result)
    predict_binary[predict_binary >= 0.5] = 1
    predict_binary[predict_binary < 0.5] = 0
    return predict_binary

if __name__ == '__main__':
    config = util.readconfig()
    model_config = config['model_params']

    # 세 가지 유형의 voxel cluster 중 하나 선택: atlas, morphome, org
    coordi_type = 'atlas'
    coordi_data = 'coordi_%s.csv' % coordi_type

    user_factor_path = os.path.join(util.checkpoint_home(), 'als_atlas_kfold_0_5_user.npy')
    item_factor_path = os.path.join(util.checkpoint_home(), 'als_atlas_kfold_0_5_item.npy')

    org_data_path = os.path.join(util.data_home(), 'binary_kfold', 'atlas', 'train_kfold_atlas_0.npy')
    org_matrix = np.load(org_data_path)

    # 선택안: keyword_origin.csv, keyword_sample.csv
    keyword_data = 'keyword_origin.csv'

    voxel_cluster_dict, voxel_cluster_count = dataload.get_voxel_cluster_dict(coordi_data)
    keyword_dict, keyword_count = dataload.get_keyword_dict(keyword_data)

    user_factor = np.load(user_factor_path)
    item_factor = np.load(item_factor_path)

    model = ALS(model_config)
    model.predict_initialize(user_factor, item_factor)

    # 여기에 원하는 키워드를 넣어주면 됨
    input_keyword = 'angry'
    predict = model.predict()
    # print(predict[keyword_dict.get(input_keyword)])
    predict_result = model.recommend(keyword_dict.get(input_keyword))

    predict_binary = binarize(predict_result)
    org_binary = org_matrix[keyword_dict.get(input_keyword)]

    # 기존에 이미 발견되었었던 상관관계는 prev_found_score에 저장
    # 새롭게 추천된 상관관계는 new_found_score에 저장
    prev_found_scores = np.zeros(len(predict_binary))
    new_found_scores = np.zeros(len(predict_binary))

    for i in range(len(org_binary)):
        if org_binary[i]==1:
            prev_found_scores[i] = predict_result[i]
        else:
            new_found_scores[i] = predict_result[i]

    print(predict_result)
    print(prev_found_scores)
    print(new_found_scores)
