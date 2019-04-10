import csv
import os


def make_sample():
    org_csv = csv.reader(open('../data/preprocessed/test.csv', 'r'))
    sample_10K = csv.writer(open('../data/preprocessed/test_10K.csv', 'w'))
    sample_10K.writerow(['voxel_id', 'keyword', 'score'])
    for i, row in enumerate(org_csv):
        if i == 0:
            continue
        elif i < 10000:
            sample_10K.writerow(row)
        else:
            break

def count_org_data():
    org_csv = csv.reader(open('../data/results/org_15M.csv', 'r'))
    count = 0
    for i, row in enumerate(org_csv):
        if i == 0:
            continue
        count += 1
    print('total row num:', count)


def find_missed_voxel():
    voxel_region_dict = {}
    coordinates_csv = csv.reader(open(os.path.abspath('../data/coordinates_table.csv'), 'r'))
    for i, row in enumerate(coordinates_csv):
        if i==0:
            continue
        voxel_region_dict.update({row[0]:int(float(row[4]))})
    contain_region_voxels = set(voxel_region_dict.keys())

    activate_data_path = '../data/preprocessed/uniformity_sorted.csv'
    activate_sample = csv.reader(open(activate_data_path, 'r'))
    missing_voxel_set = set()
    for i, row in enumerate(activate_sample):
        if i==0:
            continue
        if row[0] not in contain_region_voxels:
            missing_voxel_set.add(row[0])

    missing_voxel_list = list(missing_voxel_set)
    missing_voxel_list.sort()

    missing_voxel = '../data/results/missing_voxel.csv'
    missing_voxel_csv = csv.writer(open(missing_voxel, 'w'))
    missing_voxel_csv.writerow(['voxel_id'])
    for voxel_id in missing_voxel_list:
        missing_voxel_csv.writerow([voxel_id])


if __name__ == '__main__':
    # find_missed_voxel()
    # count_org_data()
    make_sample()