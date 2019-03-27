from sklearn.cluster import KMeans
import numpy as np

# 현재 데이터의 문제점 - 복셀 자체가 너무 많다, 너무 스파스한 데이터다
# 그래서 학습이 잘 안되는 것 같다
# 정말 그럴까????
# 목적은 잘 학습을 하는 모델을 만드는 것
# k-means clustering도 그 역할 중 하나인 것
# 그러므로 우선은 als가 잘 동작하는지를 확인해볼 필요가 있다
def kmeans_test():
    X = np.array([[1, 2, 3], [1, 4, 2], [1, 0, 5], [10, 2, 1], [10, 4, 5], [10, 0, 10]])
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    print(kmeans.labels_)
    # array([1, 1, 1, 0, 0, 0], dtype=int32)
    result = kmeans.predict([[0, 0, 5], [12, 3, 7]])
    print(result)
    # array([1, 0], dtype=int32)
    centers = kmeans.cluster_centers_
    print(centers)
    np.save('test.npy', kmeans)


def kmeans_load():
    pass


if __name__ == '__main__':
    kmeans_test()
