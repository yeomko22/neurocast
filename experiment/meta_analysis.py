import os
import csv
import numpy as np
from tqdm import tqdm
from util import util
import pandas as pd


def get_num_lines(file_path):
    logger.info('csv line counting start')
    csv_file = csv.reader(open(file_path, "r"))
    count = 0
    for i, line in enumerate(csv_file):
        if i == 0:
            continue
        count += 1
    logger.info('csv line counting finish')
    return count


def write_data(cur_keyword, positive_values, negative_values, output_csv):
    positive_count = np.size(positive_values)
    negative_count = np.size(negative_values)
    voxel_count = positive_count + negative_count

    positive_ratio = round((positive_count / voxel_count) * 100, 2)
    if positive_count != 0:
        positive_std = round(np.std(positive_values), 2)
        positive_mean = round(np.mean(positive_values), 2)
    else:
        positive_std = 0
        positive_mean = 0

    negative_ratio = round((negative_count / voxel_count) * 100, 2)
    if negative_count != 0:
        negative_std = round(np.std(negative_values), 2)
        negative_mean = round(np.mean(negative_values), 2)
    else:
        negative_std = 0
        negative_mean = 0

    output_csv.writerow([cur_keyword, voxel_count, positive_ratio, negative_ratio,
                         positive_count, positive_mean, positive_std,
                         negative_count, negative_mean, negative_std])


def count():
    # mode_list = ['train', 'test', 'total']
    mode_list = ['train']
    for mode in mode_list:
        input_path = '../data/results/{0}_origin.csv'.format(mode)
        input_csv = csv.reader(open(input_path, 'r'))

        output_path = '../data/results/{0}_origin_meta.csv'.format(mode)
        output_csv = csv.writer(open(output_path, 'w'))

        prev_keyword = None
        positive_values = np.array([])
        negative_values = np.array([])

        for i, row in tqdm(enumerate(input_csv), total=get_num_lines(input_path)):
            if i == 0:
                continue

            if not prev_keyword:
                prev_keyword = row[0]

            cur_keyword = row[0]
            if cur_keyword != prev_keyword:
                write_data(cur_keyword, positive_values, negative_values, output_csv)
                positive_values = np.array([])
                negative_values = np.array([])
                prev_keyword = cur_keyword

            cur_activation = float(row[2])
            if cur_activation > 0:
                positive_values = np.append(positive_values, cur_activation)
            else:
                negative_values = np.append(negative_values, cur_activation)

        write_data(cur_keyword, positive_values, negative_values, output_csv)

def meta_analysis():
    mode_list = ['train']
    for mode in mode_list:
        input_path = '../data/results/{0}_origin_meta.csv'.format(mode)
        df = pd.read_csv(input_path)
        print(df.head())

        # input_csv = csv.reader(open(input_path, 'r'))
        #
        # output_path = '../data/results/{0}_origin_meta_analysis.csv'.format(mode)
        # output_csv = csv.writer(open(output_path, 'w'))


if __name__ == '__main__':
    logger = util.get_logger()
    # count()
    meta_analysis()
