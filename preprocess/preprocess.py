import csv
import json
import os

import math
import nibabel as nib
from tqdm import tqdm

from util import util


# sort output csv file per voxel id (cluster same voxel id)
# it makes easier to make the data into matrix format
def sort_data(dir_name, cur_mode):
    logger.info('{0} data sort start'.format(dir_name))

    raw_data_path = os.path.join('../data/results', '%s_%s.csv' % (dir_name, cur_mode))
    sorted_data_path = os.path.join('../data/results', '%s_%s_sorted.csv' % (dir_name, cur_mode))

    raw_data = csv.reader(open(raw_data_path, 'r'))
    sorted_data = csv.writer(open(sorted_data_path, 'w'))
    sorted_data.writerow(['keyword', 'voxel_id', 'score'])

    data_list = []
    for i, row in enumerate(raw_data):
        if i==0:
            continue
        data_list.append(row)
    data_list.sort()

    for data in data_list:
        sorted_data.writerow(data)
    logger.info('{0} data sort finish'.format(dir_name))
    return sorted_data_path


# check activation score per each voxel
# if the score is over 0, write to output csv file
def voxel_check(nib_data, output_csv, keyword):
    for i in range(len(nib_data)):
        for j in range(len(nib_data[0])):
            for k in range(len(nib_data[0][0])):
                if abs(nib_data[i][j][k]) != 0.0:
                    cur_id = '%d_%d_%d' % (i, j, k)
                    cur_score = nib_data[i][j][k]
                    output_csv.writerow([keyword, cur_id, cur_score])


# read nii file per each keyword
# request voxel_check per each nii file
def process(base_dir, dir_name, keyword_list, output_csv):
    logger.info('{0} data process start'.format(dir_name))
    for i, keyword in tqdm(enumerate(keyword_list), total=len(keyword_list)):
        file_name = '%s.nii.gz' % keyword
        nib_file = nib.load(os.path.join(base_dir, dir_name, file_name))
        nib_data = nib_file.get_fdata()
        voxel_check(nib_data, output_csv, keyword)
    logger.info('{0} data process finish'.format(dir_name))


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

def main():
    # read config
    config = json.loads(open('../config.json', 'r').read())

    # set up basic path
    base_dir = os.path.abspath('../data')
    output_dir = os.path.join(base_dir, 'results')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # read keyword file and extract keyword list
    cur_mode = config['cur_mode']
    if cur_mode == 'sample':
        keyword_path = config['keyword_sample']
    else:
        keyword_path = config['keyword_origin']

    keyword_file = csv.reader(open(keyword_path, 'r'))
    keyword_list = []
    for i, keyword_line in enumerate(keyword_file):
        if i == 0:
            continue
        keyword_list.append(keyword_line[1])

    # process data per measure type
    dir_names = ['train', 'test', 'total']
    for dir_name in dir_names:
        output_path = os.path.join(output_dir, '%s_%s.csv' % (dir_name, cur_mode))
        output_csv = csv.writer(open(output_path, 'w'))
        output_csv.writerow(['keyword', 'voxel_id', 'score'])
        process(base_dir, dir_name, keyword_list, output_csv)
        sorted_data_path = sort_data(dir_name, cur_mode)
        logger.info('final result: {0}'.format(sorted_data_path))

if __name__ == '__main__':
    logger = util.get_logger()
    main()
