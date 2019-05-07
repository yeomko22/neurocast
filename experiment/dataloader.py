from scipy.sparse import csr_matrix
import csv

from tqdm import tqdm
import logging

from util import util
import numpy as np

class DataLoader:
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.keyword_dict = self.get_keyword_dict(config['data_path']['keyword_path'])

    def get_num_lines(self, file_path):
        csv_file = csv.reader(open(file_path, "r"))
        count = 0
        for i, line in enumerate(csv_file):
            if i == 0:
                continue
            count += 1
        return count

    # change raw activation score into binary labels
    def binary_preprocess(self, nii_csr_matrix):
        nii_csr_matrix.data[nii_csr_matrix.data < 0.0] = 0
        nii_csr_matrix.eliminate_zeros()
        nii_csr_matrix.data = np.ones(len(nii_csr_matrix.data))
        return nii_csr_matrix

    def get_keyword_dict(self, keyword_file_path):
        file_csv = csv.reader(open(keyword_file_path, 'r'))
        keyword_dict = {}
        for i, row in enumerate(file_csv):
            if i == 0:
                continue
            keyword_dict.update({row[1]: int(row[0])})
        return keyword_dict

    def get_filtered_coordi_matrix(self, filepath):
        # ingredients to make csr_matrix
        indptr = [0]
        indices = []
        data = []

        # meta data of csr_matrix
        vocabulary = {}
        region_id_set = set()

        self.logger.info('start to read file: {0}'.format(filepath))
        total_rows = self.get_num_lines(filepath)
        self.logger.info('total rows of data: {0}'.format(total_rows))

        self.logger.info('start to build csr_matrix')
        file_csv = csv.reader(open(filepath, 'r'))
        prev_region_id = None
        for i, row in tqdm(enumerate(file_csv), total=total_rows):
            if i == 0:
                continue
            if not prev_region_id:
                prev_region_id = row[0]
            region_id_set.add(row[0])
            index = vocabulary.setdefault(row[1], len(vocabulary))
            indices.append(index)
            data.append(row[2])

            if row[0] != prev_region_id:
                indptr.append(i - 1)
                prev_region_id = row[0]

        retion_id_list = list(region_id_set)
        retion_id_list.sort()

        nii_csr_matrix = csr_matrix((data, indices, indptr), dtype=int)

        # if you want data in binary form
        self.binary_preprocess(nii_csr_matrix)
        return retion_id_list, nii_csr_matrix, vocabulary