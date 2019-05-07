import numpy as np
import csv
import os
from util import util, dataload
import random

# 전체 데이터 셋을 k 등분하여 학습용 데이터 셋과 테스트 데이터 셋을 분리한다.
# 이 때 인풋 데이터는 0과 1로 구성된 매트릭스이다.
# 데이터 셋 분리 알고리즘
# 1. 전체 행렬에서 1 값의 개수와 인덱스를 찾는다.
# 2. 전체에서 랜덤하게 1/k개의 1 값을 누락시킨 학습용 데이터 셋을 만든다.
# 3. 이를 k번 반복하며, 이 때 학습용 데이터 셋 간에는 중복이 일어나지 않게끔 처리한다.
def kfold_split(matrix, k, coordi_type):
    coordi_list = []
    output_dir = os.path.join(util.data_home(), 'binary_kfold')
    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j]==1:
                coordi_list.append((i, j))

    random.shuffle(coordi_list)
    kfold_size = int(len(coordi_list) / k)
    print('start to generate %d fold train/test data, each size: %d' % (k, kfold_size))
    for i in range(k):
        kfold_train = np.copy(matrix)
        kfold_test = np.zeros(matrix.shape)
        for j in range(kfold_size):
            cur_coordi = coordi_list.pop()
            if not cur_coordi:
                break
            kfold_train[cur_coordi[0]][cur_coordi[1]] = 0
            kfold_test[cur_coordi[0]][cur_coordi[1]] = 1
        train_npy_path = os.path.join(output_dir, coordi_type, 'train_kfold_%s_%d.npy' % (coordi_type, i))
        test_npy_path = os.path.join(output_dir, coordi_type, 'test_kfold_%s_%d.npy' % (coordi_type, i))
        np.save(train_npy_path, kfold_train)
        np.save(test_npy_path, kfold_test)
        print('%d kfold generated' % (i+1))
    print('k-fold generate finish')

def kfold_check():
    test_kfold = np.load(os.path.join(util.data_home(), 'binary_kfold', 'test_kfold_atlas_0.npy'))
    np.savetxt('foo.csv', test_kfold.astype(int), fmt='%i', delimiter=',')
    print(test_kfold)

def timeseries_validate():
    pass

def kfold_generate():
    # 세 가지 복셀 클러스터 중 하나 선택: atlas morphome org
    coordi_type = 'org'
    coordi_data = 'coordi_%s.csv' % coordi_type

    # 선택안: keyword_origin.csv, keyword_sample.csv
    keyword_data = 'keyword_origin.csv'

    voxel_cluster_dict, voxel_cluster_count = dataload.get_voxel_cluster_dict(coordi_data)
    keyword_dict, keyword_count = dataload.get_keyword_dict(keyword_data)

    binary_matrix_data = 'matrix_%s.npy' % coordi_type
    binary_path = os.path.join(util.data_home(), 'binary_npy', binary_matrix_data)

    binary_marix = np.load(binary_path)
    kfold_split(binary_marix, 4, coordi_type)

if __name__ == '__main__':
    kfold_generate()
    # kfold_check()
