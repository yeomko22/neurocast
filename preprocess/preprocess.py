import csv

import nibabel as nib
import os


# sort output csv file per voxel id (cluster same voxel id)
# it makes easier to make the data into matrix format
def sort_data(output_dir, mtype):
    print('----- %s data sort start -----')
    raw_data_path = os.path.join(output_dir, mtype + '.csv')
    sorted_data_path = os.path.join(output_dir, mtype + '_sorted.csv')

    raw_data = csv.reader(open(raw_data_path, 'r'))
    sorted_data = csv.writer(open(sorted_data_path, 'w'))

    data_list = []
    for i, row in enumerate(raw_data):
        data_list.append(row)
    data_list.sort()

    for data in data_list:
        sorted_data.writerow(data)
    sorted_data.close()
    raw_data.close()
    print('----- %s data sort finish -----')
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
                    output_csv.writerow([cur_id, keyword, cur_score])


# read nii file per each keyword
# request voxel_check per each nii file
def process(base_dir, mtype, keyword_list, output_csv):
    print('----- %s data process start -----' % mtype)
    dir_name = 'keyword_%s_test' % mtype
    for i, keyword in enumerate(keyword_list):
        file_name = '%s_%s-test_z_FDR_0.01.nii.gz' % (keyword, mtype)
        nib_file = nib.load(os.path.join(base_dir, dir_name, file_name))
        nib_data = nib_file.get_fdata()
        voxel_check(nib_data, output_csv, keyword)
        print('%s process complete (%d/%d)' % (keyword, i, len(keyword_list)))
    output_csv.close()
    print('----- %s data process finish -----' % mtype)


def main():
    # set up basic path
    base_dir = os.path.abspath('../data')
    output_dir = os.path.join(base_dir, 'results')

    # read keyword file and extract keyword list
    keyword_file = csv.reader(open(os.path.join(base_dir, 'keyword_list.csv')))
    keyword_list = []
    for i, keyword_line in enumerate(keyword_file):
        if i == 0:
            continue
        keyword_list.append(keyword_line[1])

    # process data per measure type
    measure_types = ['uniformity', 'association']
    for mtype in measure_types:
        output_path = os.path.join(output_dir, mtype + '.csv')
        output_csv = csv.writer(open(output_path, 'w'))
        output_csv.writerow(['voxel_id', 'keyword', 'score'])
        process(base_dir, mtype, keyword_list, output_csv)
        sorted_data_path = sort_data(output_dir, mtype)
        print('final result: %s' % sorted_data_path)


if __name__ == '__main__':
    main()
