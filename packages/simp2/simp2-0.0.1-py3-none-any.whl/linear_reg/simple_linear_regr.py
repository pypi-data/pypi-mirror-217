import os.path

import numpy as np
from simple_linear_regr_utils import generate_data, evaluate
import pickle


class SimpleLinearRegression:
    def __init__(self, iterations=15000, lr=0.1):
        self.iterations = iterations  # number of iterations the fit method will be called
        self.lr = lr  # The learning rate
        self.losses = []  # A list to hold the history of the calculated losses
        self.W, self.b = None, None  # the slope and the intercept of the model

    def __loss(self, y, y_hat):
        """

        :param y: the actual output on the training set
        :param y_hat: the predicted output on the training set
        :return:
            loss: the sum of squared error

        """
        # ToDO calculate the loss. use the sum of squared error formula for simplicity
        # loss = np.square(np.subtract(y, y_hat)).mean()
        loss = ((y - y_hat) ** 2).mean()
        self.losses.append(loss)
        return loss

    def __init_weights(self, X):
        """

        :param X: The training set
        """
        weights = np.random.normal(size=X.shape[1] + 1)
        self.W = weights[:X.shape[1]].reshape(-1, X.shape[1])
        self.b = weights[-1]

    def __sgd(self, X, y, y_hat):
        """

        :param X: The training set
        :param y: The actual output on the training set
        :param y_hat: The predicted output on the training set
        :return:
            sets updated W and b to the instance Object (self)
        """
        # ToDo calculate dW & db.
        N = X.shape[0]
        for i in range(N):
            dW = -(2 / N) * X[i] * (y[i] - y_hat[i])
            db = -(2 / N) * (y[i] - y_hat[i])
            #  ToDO update the self.W and self.b using the learning rate and the values for dW and db
            self.W = self.W - self.lr * dW
            self.b = self.b - self.lr * db

    def fit(self, X, y):
        """

        :param X: The training set
        :param y: The true output of the training set
        :return:
        """
        self.__init_weights(X)
        y_hat = self.predict(X)
        loss = self.__loss(y, y_hat)
        print(f"Initial Loss: {loss}")
        for i in range(self.iterations + 1):
            self.__sgd(X, y, y_hat)
            y_hat = self.predict(X)
            loss = self.__loss(y, y_hat)
            if not i % 100:
                print(f"Iteration {i}, Loss: {loss}")

    def predict(self, X):
        """

        :param X: The training dataset
        :return:
            y_hat: the predicted output
        """
        # ToDO calculate the predicted output y_hat. remember the function of a line is defined as y = WX + b
        N = X.shape[0]
        y_hat = list()
        for i in range(N):
            y = (np.dot(self.W, X[i]) + self.b).item()
            y_hat.append(y)
        return np.array(y_hat)[:, np.newaxis]


if __name__ == "__main__":
    X_train, y_train, X_test, y_test = generate_data()
    model = SimpleLinearRegression()
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    evaluate(model, X_test, y_test, predicted)

    # save trained model
    model_path = os.path.join("saved_model", "linear_model.dat")

    with open(model_path, 'wb') as saved_model:
        pickle.dump(model, saved_model)

    # reload model
    with open(model_path, 'rb') as raw_model:
        reload_model = pickle.load(raw_model)
    evaluate(reload_model, X_test, y_test, predicted)
