import implicit

from util import util
from model.als import ALS
import os

import numpy as np
import logging

class InvalidModelException(Exception):
    pass


def get_logger():
    logger = logging.getLogger("experiment")
    if logger.handlers:
        logger.handlers.clear()

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)
    return logger


def initialize_model(model_config, rating_matrix, validation):
    if model_config['model'] == 'als':
        model = ALS(model_config)
        model.train_initialize(rating_matrix, validation)
    else:
        raise InvalidModelException
    return model

# 학습을 진행하는 함수
# 모델 이름을 정하고, 로스 펑션을 시각화하는 역할을 한다.
# 실제 트레이닝 코드는 모델 안에 정의되어 있다. 이는 모델별로 최적화 알고리즘이 다르기 때문이다.
def train(model, model_config, etc_info):
    model_name = '{0}_{1}_{2}_{3}'.format(model_config['model'],
                                          model_config['voxel_cluster_type'],
                                          model_config['validate_type'],
                                          etc_info)
    model.model_name = model_name
    logger.info('{0} start to train'.format(model_name))
    predict_errors, confidence_errors, regularization_list, \
    total_losses, accuracy_list, random_list = model.fit()
    model.plot_losses(predict_errors, confidence_errors, regularization_list, total_losses, accuracy_list, random_list)
    logger.info('{0} finish train finish'.format(model_name))

# k-fold 검증 방식을 사용하여 모델 학습을 진행
def train_kfold(model_config):
    validate_k = model_config['validate_k']
    coordi_type = model_config['voxel_cluster_type']
    for i in range(validate_k):
        train_matrix_data = 'train_kfold_%s_%d.npy' % (coordi_type, i)
        train_matrix_path = os.path.join(util.data_home(), 'binary_kfold', coordi_type, train_matrix_data)
        train_matrix = np.load(train_matrix_path)

        validation_matrix_data = 'test_kfold_%s_%d.npy' % (coordi_type, i)
        validation_matrix_path = os.path.join(util.data_home(), 'binary_kfold', coordi_type, validation_matrix_data)
        validation_matrix = np.load(validation_matrix_path)

        # 모델을 초기화 한 다음에 학습을 진행한다.
        # 로스 변화 시각화는 train 함수에서 실행하며, 모델의 저장은 각 모델 클래스 파일에 정의되어 있다.
        model = initialize_model(model_config, train_matrix, validation_matrix)
        train(model, model_config, i)
        logger.info('train and save model')
        print('kfold step %d finish' % i)

def train_timeseries(model_config):
    pass

def main():
    config = util.readconfig()
    model_config = config['model_params']

    if model_config['validate_type'] == 'kfold':
        train_kfold(model_config)
    elif model_config['validate_type'] == 'timeseires':
        train_timeseries(model_config)

if __name__ == '__main__':
    logger = get_logger()
    main()
