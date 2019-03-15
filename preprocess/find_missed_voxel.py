import csv
import os


def find_missed_voxel():
    voxel_region_dict = {}
    coordinates_csv = csv.reader(open(os.path.abspath('../data/coordinates_table.csv'), 'r'))
    for i, row in enumerate(coordinates_csv):
        if i==0:
            continue
        voxel_region_dict.update({row[0]:int(float(row[4]))})
    contain_region_voxels = set(voxel_region_dict.keys())

    activate_data_path = '../data/results/uniformity_sorted.csv'
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
    find_missed_voxel()
