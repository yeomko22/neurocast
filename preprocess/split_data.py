import csv
import os

# Todo: 추후에 복셀 영역별 데이터 셋을 구축해야할 필요성이 생기면 적용할 것 (아마 안할 듯)
# class VoxelRegion:
#     def __init__(self, region_id):
#         self.region_id = region_id
#         self.score_dict = {}
#         self.voxel_set = set()
#
#     def set_score(self, voxel_id, keyword, score):
#         self.voxel_set.add(voxel_id)
#         if not self.score_dict.keys().__contains__(keyword):
#             self.score_dict.update({keyword: 0.0})
#         self.score_dict.update({keyword: self.score_dict.get(keyword) + float(score)})
#
#     def info(self):
#         print(self.region_id)
#         print(self.score_dict)
#         print(self.voxel_set)
#
#
# def make_sample_coordinates():
#     coordiates_csv = csv.reader(open(os.path.abspath('../data/coordinates_table.csv'), 'r'))
#     coordiates_sample = csv.writer(open(os.path.abspath('../data/coordinates_sample.csv'), 'w'))
#     for i, row in enumerate(coordiates_csv):
#         if i > 20:
#             break
#         coordiates_sample.writerow(row)

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
