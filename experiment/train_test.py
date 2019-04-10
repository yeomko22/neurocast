import numpy as np
from scipy.sparse import coo_matrix
import implicit.als

X = np.random.randint(5, size=(100, 200))
X0 = coo_matrix(X, dtype=np.float)
model = implicit.als.AlternatingLeastSquares(factors=50, iterations=10, calculate_training_loss=True, regularization=10)
model.fit(X0)
print('============================')
print(model.user_factors)
