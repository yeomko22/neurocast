import os
import csv
from util import util
import pandas as pd


def get_keyword_dict(keyword_data):
    keyword_path = os.path.join(util.data_home(), 'keyword', keyword_data)
    keyword_csv = csv.reader(open(keyword_path, 'r'))
    keyword_dict = {}
    keyword_count = 0
    for i, row in enumerate(keyword_csv):
        if i==0:
            continue
        if not keyword_dict.keys().__contains__(row[1]):
            keyword_dict.update({row[1]: keyword_count})
            keyword_count += 1
        else:
            print('dupli!', row)
    return keyword_dict, keyword_count


def get_voxel_cluster_dict(coordi_data):
    coordi_path = os.path.join(util.data_home(), 'coordi', coordi_data)
    coordi_df = pd.read_csv(coordi_path)
    coordi_df = coordi_df.drop(columns=['mni_x', 'mni_y', 'mni_z'])

    # 기존 코디네이트 테이블이 1번부터 region index를 매겼기 때문에 1씩 빼준다.
    coordi_df['shen_regionid'] = (coordi_df['shen_regionid'].astype('int64') - 1)
    coordi_df = coordi_df.set_index('voxel_id')

    # max 값에 + 1을 취해주는 것은 각 인덱스를 모조리 -1 해주었기 때문에 0부터 시작한다 그러므로 +1을 해주어야 전체 개수가 된다.
    return coordi_df.to_dict()['shen_regionid'], int(coordi_df['shen_regionid'].max()) + 1
