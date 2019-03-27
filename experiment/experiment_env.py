import implicit

from experiment.dataloader import DataLoader
import json
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


def initialize_model(config):
    if config['model'] == 'als':
        model = implicit.als.AlternatingLeastSquares(factors=config['feature_dim'],
                                                     regularization=config['norm-lambda'],
                                                     calculate_training_loss=True)
    else:
        raise InvalidModelException
    return model


def train(config, train_voxel_ids, train_csr_matrix, train_vocabulary):
    model_name = '{0}_{1}_{2}_{3}'.format(config['model'], config['feature_dim'],
                                          config['confidence-weight'], config['norm-lambda'])
    logger.info('{0} start to train'.format(model_name))
    model = initialize_model(config)
    model.fit(train_csr_matrix)
    model_output_path = '../data/checkpoint/{0}'.format(model_name)
    np.save(model_output_path, model)
    logger.info('{0} finish train finish and saved'.format(model_name))

    user_items = train_csr_matrix.T.tocsr()
    recommended_list = model.recommend('angry', user_items)
    logger.info(recommended_list)
    return model

def main():
    config = json.loads(open('../config.json', 'r').read())
    cur_mode = config['cur_mode']
    if cur_mode == 'sample':
        train_path = os.path.abspath(config['train_sample'])
        test_path = os.path.abspath(config['test_sample'])
    else:
        train_path = os.path.abspath(config['train_origin'])
        test_path = os.path.abspath(config['test_origin'])

    dataloader = DataLoader(logger)
    train_voxel_ids, train_csr_matrix, train_vocabulary = dataloader.get_csr_matrix(train_path)
    # test_voxel_ids, test_csr_matrix, test_vocabulary = dataloader.get_csr_matrix(test_path)

    trained_model = train(config, train_voxel_ids, train_csr_matrix, train_vocabulary)
    trained_model.recommend()

if __name__ == '__main__':
    logger = get_logger()
    main()
