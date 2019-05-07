'''
파일 목적
input: 각 유형별 coordinate table 파일
데이터 처리 : 각 복셀별로 클러스터링 한 뒤, 특정 키워드가 해당 복셀에서 얼만큼 활성화되었는 지를 카운팅
           이 때 카운팅 숫자가 config 파일 내의 positive limit을 넘어설 경우 1 아니면 0으로 binarize 적용
output: 복셀 클러스터 개수 x 키워드 크기의 numpy matrix
        이를 파일의 형태로 저장하며 위치는 /data/coordi_`type`.npy 로 저장된다.

setting
main 함수 안에서 input으로 전달할 coordinate_table과 원본 데이터 명을 집어넣는다.
어떠한 후보군이 있는지는 main 함수 위에 주석으로 작성되어있다.
'''


import csv
import os

import numpy as np
from tqdm import tqdm

from util import util, dataload


def get_input_data(input_data):
    input_path = os.path.join(util.data_home(), 'origin', input_data)
    return csv.reader(open(input_path, 'r'))


def get_num_lines(input_data):
    print('start read line num')
    input_path = os.path.join(util.data_home(), 'origin', input_data)
    csv_file = csv.reader(open(input_path, "r"))
    count = 0
    for i, line in enumerate(csv_file):
        if i == 0:
            continue
        count += 1
    return count


def main():
    config = (util.readconfig())['preprocess']
    data_dir = os.path.join(util.project_home(), 'data', 'origin')

    # 입력 데이터 설정
    # 선택안: train_origin.csv, test_origin.csv, total_origin.csv
    input_data = 'train_origin.csv'

    # 세 가지 유형의 voxel cluster 중 하나 선택: atlas, morphome, org
    coordi_type = 'org'
    coordi_data = 'coordi_%s.csv' % coordi_type

    # 선택안: keyword_origin.csv, keyword_sample.csv
    keyword_data = 'keyword_origin.csv'

    input_csv = get_input_data(input_data)
    voxel_cluster_dict, voxel_cluster_count = dataload.get_voxel_cluster_dict(coordi_data)
    keyword_dict, keyword_count = dataload.get_keyword_dict(keyword_data)

    matrix = np.zeros([keyword_count, voxel_cluster_count])
    for i, row in tqdm(enumerate(input_csv), total=get_num_lines(input_data)):
        if i==0:
            continue

        if not voxel_cluster_dict.get(row[1]):
            continue

        row_coord = keyword_dict.get(row[0])
        col_coord = voxel_cluster_dict.get(row[1])
        matrix[row_coord][col_coord] += 1

    # 특정 임계치 이상 언급 횟수가 있으면 1, 아니면 0으로 정규화해준다.
    if config['binarize']:
        matrix[matrix < config['positive_limit']] = 0
        matrix[matrix >= config['positive_limit']] = 1

    # 결과 numpy array를 파일 형태로 저장한다.
    np_path = os.path.join(os.path.join(util.data_home(), 'binary_npy', 'matrix_%s.npy' % coordi_type))
    np.save(np_path, matrix)

if __name__ == '__main__':
    main()
