import numpy as np
from matplotlib import pyplot as plt
from util import util
import os

class ALS:
    def __init__(self, model_config):
        self.model_name = None
        self.model_config = model_config
        self.R = None
        self.validation = None
        self.nu = None
        self.ni = None
        self.nf = None
        self.X = None
        self.Y = None
        self.P = None
        self.C = None
        self.r_lambda = None

    def train_initialize(self, rating_matrix, validation):
        self.R = rating_matrix
        self.validation = validation
        self.nu = self.R.shape[0]
        self.ni = self.R.shape[1]
        self.nf = self.model_config['feature_dim']
        self.X = np.random.rand(self.nu, self.nf) * 0.01
        self.Y = np.random.rand(self.ni, self.nf) * 0.01

        self.P = np.copy(self.R)
        self.P[self.P > 0] = 1
        self.C = 1 + self.model_config['confidence_alpha'] * self.R
        self.r_lambda = self.model_config['norm_lambda']

    def predict_initialize(self, user_factor, item_factor):
        self.X = user_factor
        self.Y = item_factor

    def loss_function(self, C, P, xTy, X, Y, r_lambda):
        predict_error = np.square(P - xTy)
        confidence_error = np.sum(C * predict_error)
        regularization = r_lambda * (np.sum(np.square(X)) + np.sum(np.square(Y)))
        total_loss = confidence_error + regularization
        return np.sum(predict_error), confidence_error, regularization, total_loss

    def optimize_user(self, X, Y, C, P, nu, nf, r_lambda):
        yT = np.transpose(Y)
        for u in range(nu):
            Cu = np.diag(C[u])
            yT_Cu_y = np.matmul(np.matmul(yT, Cu), Y)
            lI = np.dot(r_lambda, np.identity(nf))
            yT_Cu_pu = np.matmul(np.matmul(yT, Cu), P[u])
            X[u] = np.linalg.solve(yT_Cu_y + lI, yT_Cu_pu)

    def optimize_item(self, X, Y, C, P, ni, nf, r_lambda):
        xT = np.transpose(X)
        for i in range(ni):
            Ci = np.diag(C[:, i])
            xT_Ci_x = np.matmul(np.matmul(xT, Ci), X)
            lI = np.dot(r_lambda, np.identity(nf))
            xT_Ci_pi = np.matmul(np.matmul(xT, Ci), P[:, i])
            Y[i] = np.linalg.solve(xT_Ci_x + lI, xT_Ci_pi)

    def plot_losses(self, predict_errors, confidence_errors, regularization_list, total_losses, accuracy_list, random_list):
        plt.subplots_adjust(wspace=100.0, hspace=30.0)
        fig = plt.figure()
        fig.set_figheight(30)
        fig.set_figwidth(10)

        total_loss_line = fig.add_subplot(2, 2, 1)
        predict_error_line = fig.add_subplot(2, 2, 2)
        confidence_error_line = fig.add_subplot(2, 2, 3)
        accuracy_line = fig.add_subplot(2, 2, 4)

        predict_error_line.set_title("Predict Error")
        predict_error_line.plot(predict_errors)

        confidence_error_line.set_title("Confidence Error")
        confidence_error_line.plot(confidence_errors)


        total_loss_line.set_title("Total Loss")
        total_loss_line.plot(total_losses)

        accuracy_line.set_title("Cross Validation Accuracy")
        accuracy_line.plot(accuracy_list)
        plt.show()

    def get_accuracy(self, predict):
        rows, cols = predict.shape
        count_wrong = 0
        count_correct = 0
        for i in range(rows):
            for j in range(cols):
                if self.validation[i][j] == 0:
                    continue
                if self.validation[i][j] == predict[i][j]:
                    count_correct += 1
                else:
                    count_wrong += 1
        return count_correct, count_wrong

    def save_model(self, epoch):
        user_factor_path = os.path.join(util.data_home(), 'checkpoint', '%s_%d_user.npy' % (self.model_name, epoch))
        item_factor_path = os.path.join(util.data_home(), 'checkpoint', '%s_%d_item.npy' % (self.model_name, epoch))
        np.save(user_factor_path, self.X)
        np.save(item_factor_path, self.Y)
        print("checkpoint saved!")

    def fit(self):
        predict_errors = []
        confidence_errors = []
        regularization_list = []
        total_losses = []
        accuracy_list = []
        random_accuracy_list = []

        for i in range(15):
            if i != 0:
                self.optimize_user(self.X, self.Y, self.C, self.P, self.nu, self.nf, self.r_lambda)
                self.optimize_item(self.X, self.Y, self.C, self.P, self.ni, self.nf, self.r_lambda)
            predict = np.matmul(self.X, np.transpose(self.Y))
            predict_error, confidence_error, regularization, total_loss = self.loss_function(self.C, self.P, predict,
                                                                                             self.X, self.Y, self.r_lambda)
            predict_errors.append(predict_error)
            confidence_errors.append(confidence_error)
            regularization_list.append(regularization)
            total_losses.append(total_loss)

            predict = self.predict()
            # 기존에 학습했던 키워드들에 대한 예측값들은 모두 제외한다.
            predict = predict - self.R
            predict[predict < 0] = 0
            RMSE = np.sqrt(np.mean((self.validation - predict) ** 2))

            predict[predict > 0.5] = 1

            count_correct, count_wrong = self.get_accuracy(predict)
            random_correct, random_wrong = self.get_accuracy(np.random.randint(2, size=(self.R.shape[0], self.R.shape[1])))

            accuracy = round((count_correct / (count_correct + count_wrong)) * 100, 2)
            random_accuracy = round((random_correct / (random_correct + random_wrong)) * 100, 2)
            random_accuracy_list.append(random_accuracy)
            accuracy_list.append(accuracy)
            print('==========================================')
            print("predict error: %f" % predict_error)
            print("confidence error: %f" % confidence_error)
            print("total loss: %f" % total_loss)
            print('\ntotoal predict: %d' % predict.sum())
            print("validation RMSE: %f" % RMSE)
            print("validation accuracy: %f" % accuracy)
            print("random accuracy: %f" % random_accuracy)
            print('==========================================')

            if (i+1) % 5 == 0:
                self.save_model(i+1)

        return  predict_errors,  confidence_errors, regularization_list, total_losses, accuracy_list, random_accuracy_list

    def predict(self):
        return np.matmul(self.X, np.transpose(self.Y))

    def recommend(self, keyword_index):
        return np.matmul(self.X[keyword_index], np.transpose(self.Y))
