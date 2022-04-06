import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from pathlib import Path

def accuracy(y, pred):
    return np.sum(y == pred) / float(len(y))

def parse_spambase_data(filename):
    """ Given a filename return X and Y numpy arrays

    X is of size number of rows x num_features
    Y is an array of size the number of rows
    Y is the last element of each row. (Convert 0 to -1)
    """
    ### BEGIN SOLUTION
    df = pd.read_csv(filename, header=None)
    X = df.iloc[:, :-1].to_numpy()
    Y = df.iloc[:, -1].to_numpy()
    Y = np.where(Y == 0, -1, Y)

    ### END SOLUTION
    return X, Y


def adaboost(X, y, num_iter, max_depth=1):
    """Given an numpy matrix X, a array y and num_iter return trees and weights 
   
    Input: X, y, num_iter
    Outputs: array of trees from DecisionTreeClassifier
             trees_weights array of floats
    Assumes y is {-1, 1}
    """
    trees = []
    trees_weights = [] 
    N, _ = X.shape
    d = np.ones(N) / N

    ### BEGIN SOLUTION
    for i in range(num_iter):
        h = DecisionTreeClassifier(max_depth=max_depth, random_state=0)
        if i == 0:
            w = d
        h.fit(X, y, sample_weight=w)
        y_pred = h.predict(X)
        misclass_weights = w[y_pred != y]
        err = np.sum(misclass_weights) / np.sum(w)
        alpha = np.log((1-err+0.01)/(err+0.01))
        w = np.where(y_pred != y, w*np.exp(alpha), w)

        trees.append(h)
        trees_weights.append(alpha)
    ### END SOLUTION
    return trees, trees_weights


def adaboost_predict(X, trees, trees_weights):
    """Given X, trees and weights predict Y
    """
    # X input, y output
    N, _ =  X.shape
    y = np.zeros(N)
    ### BEGIN SOLUTION
    y_preds = np.array([tree.predict(X) for i, tree in enumerate(trees)])
    y = np.sign(np.sum(y_preds.T * trees_weights, axis=1))
    ### END SOLUTION
    return y
