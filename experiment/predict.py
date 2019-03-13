import implicit
from implicit.nearest_neighbours import bm25_weight
import dataloader
import numpy as np


def main():
    filepath = './data/results/sample.csv'
    voxel_id_list, csr_matrix = dataloader.get_csr_matrix(filepath)
    min_rating = -3
    csr_matrix.data[csr_matrix.data < min_rating] = 0
    csr_matrix.eliminate_zeros()
    csr_matrix.data = np.ones(len(csr_matrix.data))

    # Todo: how to normalize and weight brain nii sparse matrix
    csr_matrix = (bm25_weight(csr_matrix, B=0.9) * 5).tocsr()
    model = implicit.als.AlternatingLeastSquares(factors=50)
    model.fit(csr_matrix)

    # Todo: how to get recomment result
    user_items = csr_matrix.T.tocsr()
    recommendations = model.recommend(voxel_id_list, user_items)
    print(recommendations)


if __name__ == '__main__':
    main()
