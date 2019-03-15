import csv

import nibabel as nib
import os
from tqdm import tqdm
from util import util

# sort output csv file per voxel id (cluster same voxel id)
# it makes easier to make the data into matrix format
def sort_data(output_dir, mtype):
    logger.info('{0} data sort start'.format(mtype))

    raw_data_path = os.path.join(output_dir, mtype + '.csv')
    sorted_data_path = os.path.join(output_dir, mtype + '_sorted.csv')

    raw_data = csv.reader(open(raw_data_path, 'r'))
    sorted_data = csv.writer(open(sorted_data_path, 'w'))
    sorted_data.writerow(['voxel_id', 'keyword', 'score'])

    data_list = []
    for i, row in enumerate(raw_data):
        if i==0:
            continue
        data_list.append(row)
    data_list.sort()

    for data in data_list:
        sorted_data.writerow(data)
    logger.info('{0} data sort finish'.format(mtype))
    return sorted_data_path


# check activation score per each voxel
# if the score is over 0, write to output csv file
def voxel_check(nib_data, output_csv, keyword):
    for i in range(len(nib_data)):
        for j in range(len(nib_data[0])):
            for k in range(len(nib_data[0][0])):
                if nib_data[i][j][k] > 0.0:
                    cur_id = '%d_%d_%d' % (i, j, k)
                    cur_score = nib_data[i][j][k]
                    output_csv.writerow([cur_id, keyword, cur_score])


# read nii file per each keyword
# request voxel_check per each nii file
def process(base_dir, mtype, keyword_list, output_csv):
    logger.info('{0} data process start'.format(mtype))
    dir_name = 'keyword_%s_test' % mtype

    for i, keyword in tqdm(enumerate(keyword_list), total=len(keyword_list)):
        file_name = '%s_%s-test_z_FDR_0.01.nii.gz' % (keyword, mtype)
        nib_file = nib.load(os.path.join(base_dir, dir_name, file_name))
        nib_data = nib_file.get_fdata()
        voxel_check(nib_data, output_csv, keyword)
    logger.info('{0} data process finish'.format(mtype))


def main():
    # set up basic path
    base_dir = os.path.abspath('../data')
    output_dir = os.path.join(base_dir, 'results')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # read keyword file and extract keyword list
    keyword_file = csv.reader(open(os.path.join(base_dir, 'keyword_list.csv')))
    keyword_list = []
    for i, keyword_line in enumerate(keyword_file):
        if i == 0:
            continue
        keyword_list.append(keyword_line[1])

    # process data per measure type
    measure_types = ['uniformity']
    for mtype in measure_types:
        output_path = os.path.join(output_dir, mtype + '.csv')
        output_csv = csv.writer(open(output_path, 'w'))
        output_csv.writerow(['voxel_id', 'keyword', 'score'])
        process(base_dir, mtype, keyword_list, output_csv)
        sorted_data_path = sort_data(output_dir, mtype)
        logger.info('final result: {0}'.format(sorted_data_path))

if __name__ == '__main__':
    logger = util.get_logger()
    main()
