from scipy.sparse import csr_matrix
import csv

from tqdm import tqdm
import logging


def get_num_lines(file_path):
    csv_file = csv.reader(open(file_path, "r"))
    count = 0
    for i, line in enumerate(csv_file):
        if i == 0:
            continue
        count += 1
    return count


def get_csr_matrix(filepath):
    indptr = [0]
    indices = []
    data = []
    vocabulary = {}
    voxel_id_set = set()

    total_rows = get_num_lines(filepath)
    logging.info('total rows of data: {0}'.format(total_rows))

    file_csv = csv.reader(open(filepath, 'r'))
    prev_voxel_id = None
    for i, row in tqdm(enumerate(file_csv), total=get_num_lines(filepath)):
        if i == 0:
            continue
        if not prev_voxel_id:
            prev_voxel_id = row[0]
        voxel_id_set.add(row[0])
        index = vocabulary.setdefault(row[1], len(vocabulary))
        indices.append(index)
        data.append(float(row[2].replace('\\', '')))

        if row[0] != prev_voxel_id:
            indptr.append(i - 1)
            prev_voxel_id = row[0]
    voxel_id_list = list(voxel_id_set)
    voxel_id_list.sort()
    nii_csr_matrix = csr_matrix((data, indices, indptr), dtype=int)
    return voxel_id_list, nii_csr_matrix
