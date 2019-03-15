from scipy.sparse import csr_matrix
import csv

from tqdm import tqdm
import logging

from util import util

class DataLoader:
    def get_num_lines(self, file_path):
        csv_file = csv.reader(open(file_path, "r"))
        count = 0
        for i, line in enumerate(csv_file):
            if i == 0:
                continue
            count += 1
        return count

    def get_csr_matrix(self, filepath):
        # ingredients to make csr_matrix
        indptr = [0]
        indices = []
        data = []

        # meta data of csr_matrix
        vocabulary = {}
        voxel_id_set = set()

        logger = util.get_logger()
        logger.info('start to read file: {0}'.format(filepath))
        total_rows = self.get_num_lines(filepath)
        logger.info('total rows of data: {0}'.format(total_rows))

        logger.info('start to build csr_matrix')
        file_csv = csv.reader(open(filepath, 'r'))
        prev_voxel_id = None
        for i, row in tqdm(enumerate(file_csv), total=total_rows):
            if i == 0:
                continue
            if not prev_voxel_id:
                prev_voxel_id = row[0]
            voxel_id_set.add(row[0])
            index = vocabulary.setdefault(row[1], len(vocabulary))
            indices.append(index)
            data.append(float(row[2].replace('\\', '')))

            if row[0] != prev_voxel_id:
                indptr.append(i - 1)
                prev_voxel_id = row[0]
        voxel_id_list = list(voxel_id_set)
        voxel_id_list.sort()
        nii_csr_matrix = csr_matrix((data, indices, indptr), dtype=int)
        return voxel_id_list, nii_csr_matrix, vocabulary
